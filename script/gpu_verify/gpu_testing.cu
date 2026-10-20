// Copyright 2026 Seth Troisi
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <atomic>
#include <cassert>
#include <chrono>
#include <csignal>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <memory>
#include <mutex>
#include <thread>
#include <vector>

// pthread_setname_np
#include <pthread.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gmp.h>

#include "miller_rabin.h"

using namespace std::chrono;
using std::cout;
using std::endl;
using std::vector;
namespace py = pybind11;

//*************************************************************************** //
//**********************************GLOBALS********************************** //

// Can't import gpu_testing because it needs to import gap_seach_gpu.h / GPUBatch

#ifdef GPU_BITS
const int BITS = GPU_BITS;
#else
const int BITS = 1024;
#endif

const int WINDOW_BITS = 4 + (BITS > 256) + (BITS > 512);
const int THREADS_PER_INSTANCE = (BITS <= 512) ? 4 : 8;
const size_t GPU_BATCH_SIZE = 8 * 1024;


std::atomic<bool> is_running{false};
std::mutex merge_mtx;
std::atomic<uint32_t> tests_run{0};

//**********************************GLOBALS********************************** //
//*************************************************************************** //

typedef mr_params_t<THREADS_PER_INSTANCE, BITS, WINDOW_BITS> gpu_params;

class GPUBatch {
    public:
        // current index.
        size_t i;

        // number to check if prime
        vector<mpz_t*> z;
        // XXX: This is an ugly hack because you can't create mpz_t vector easily
        mpz_t *z_array;

        // If z[i] should be tested
        vector<uint8_t>  active;
        // gap, negative for start and end
        vector<int32_t> gap;
        // Result from GPU
        vector<int>  result;

        explicit GPUBatch(size_t n) {
            elements = n;

            z_array = (mpz_t *) malloc(n * sizeof(mpz_t));
            for (size_t i = 0; i < n; i++) {
                mpz_init(z_array[i]);
                z.push_back(&z_array[i]);
            }

            gap.resize(n, 0);
            active.resize(n, 0);
            result.resize(n, -1);
        }

        ~GPUBatch() {
            //cout << "~GPUBatch" << endl;
            for (size_t i = 0; i < elements; i++) {
                mpz_clear(z_array[i]);
            }
            free(z_array);
        }

        GPUBatch(const GPUBatch&) = delete;
        GPUBatch& operator=(const GPUBatch&) = delete;

        void run() {
            runner.run_test(i, z, result);
        }
    private:
        test_runner_t<gpu_params> runner{GPU_BATCH_SIZE};

        size_t capacity() const {
            return elements;
        }
    private:
        size_t elements;
};



inline void fill_batch(GPUBatch& batch, vector<uint32_t> offsets) {
    batch.i = 0;
    // Turn off all entries in batch
    std::fill_n(batch.active.begin(), GPU_BATCH_SIZE, false);
    // Mark all results as invalid
    std::fill_n(batch.result.begin(), GPU_BATCH_SIZE, -1);

    {
        assert( test_data.state == TestData::ACTIVE );
        uint32_t gpu_i = batch.i;  // [GPU] batch index
        size_t j = test_data.test_i;
        for (; j < test_data.unknown_m_i.size() && gpu_i < GPU_BATCH_SIZE; j++) {
            // Skip any element where a previous prime was found.
            // Happens when primes from last X weren't removed from active_m before sieve started.
            uint32_t m_i = test_data.unknown_m_i[j];
            uint32_t index = m_i >> 1;

            // Should happen only with a few primes found in last X.
            if (test_data.found_prime_m_i[index >> 5] & (1 << (index & 31)))
                continue;

            batch.active[gpu_i] = true;
            batch.m_i[gpu_i] = m_i;
            gpu_i++;
        }

        test_data.test_i = j;
        batch.i = gpu_i;
    }

    assert( batch.i <= GPU_BATCH_SIZE);
}


void signal_callback_handler(int) {
    if (is_running == 1) {
       cout << endl;
       cout << "Caught CTRL+C stopping" << endl;
       is_running = 0;
    } else {
       cout << "Caught 2nd CTRL+C, exit(2) now." << endl;
       exit(2);
       exit(2);
    }
}

int main(int argc, char* argv[]) {
    printf("TESTING PRIMES ON GPU\n");
    printf("BITS=%d\n", BITS);
    printf("PRP/BATCH=%ld\n", GPU_BATCH_SIZE);
    printf("THREADS/PRP=%d\n", THREADS_PER_INSTANCE);
    setlocale(LC_NUMERIC, "");

    is_running = true;

    // Setup CTRL+C catcher
    signal(SIGINT, signal_callback_handler);

    auto start_t = high_resolution_clock::now();

    GPUBatch batch(GPU_BATCH_SIZE);

    mpz_t tmp;
    mpz_init(tmp);
    std::ifstream f("to_test.txt");
    uint32_t gap;
    std::string start;

    while (is_running) {
        // Queue and run next batch
        while (f >> gap >> start) {
            mpz_set_str(tmp);
        }

        double total_t = duration<double>(high_resolution_clock::now() - start_t).count();
        printf("\ttotal tests     : %'u (%'u/sec)\n",
                tests_run.load(), (uint32_t) (tests_run / total_t));
    }

    mpz_clear(tmp);

    double total_t = duration<double>(high_resolution_clock::now() - start_t).count();
    setlocale(LC_NUMERIC, "");
    printf("\nGPU Timings (%.0f seconds):\n", total_t);
    printf("\ttotal tests     : %'u (%'u/sec)\n",
            tests_run.load(), (uint32_t) (tests_run / total_t));
    printf("\n");
    setlocale(LC_NUMERIC, "C");
}
