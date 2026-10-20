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
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <memory>
#include <thread>
#include <vector>

// pthread_setname_np
#include <pthread.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gmp.h>

#include "miller_rabin.h"

using std::vector;
namespace py = pybind11;

//*************************************************************************** //
//**********************************GLOBALS********************************** //

// Can't import gpu_testing because it needs to import gap_seach_gpu.h / GPUBatch

const size_t GPU_BATCH_SIZE = 4 * 1024;


std::atomic<uint32_t> tests_run{0};

//**********************************GLOBALS********************************** //
//*************************************************************************** //

typedef mr_params_t<4,  512, 5> params_512;
typedef mr_params_t<8, 1024, 6> params_1024;
typedef mr_params_t<8, 2048, 7> params_2048;
typedef mr_params_t<16, 4096, 8> params_4096;

test_runner_t<params_512>  runner_512{GPU_BATCH_SIZE};
test_runner_t<params_1024> runner_1024{GPU_BATCH_SIZE};
test_runner_t<params_2048> runner_2048{GPU_BATCH_SIZE};
test_runner_t<params_4096> runner_4096{GPU_BATCH_SIZE};

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
        vector<uint32_t> offset;
        // Result from GPU
        vector<int>  result;

        explicit GPUBatch(size_t n) {
            elements = n;

            z_array = (mpz_t *) malloc(n * sizeof(mpz_t));
            for (size_t i = 0; i < n; i++) {
                mpz_init(z_array[i]);
                z.push_back(&z_array[i]);
            }

            offset.resize(n, 0);
            active.resize(n, 0);
            result.resize(n, -1);
        }

        ~GPUBatch() {
            //printf("~GPUBatch\n");
            for (size_t i = 0; i < elements; i++) {
                mpz_clear(z_array[i]);
            }
            free(z_array);
        }

        GPUBatch(const GPUBatch&) = delete;
        GPUBatch& operator=(const GPUBatch&) = delete;

        void reset() {
            i = 0;
            // Turn off all entries in batch
            std::fill_n(active.begin(), GPU_BATCH_SIZE, false);
            // Mark all results as invalid
            std::fill_n(result.begin(), GPU_BATCH_SIZE, -1);
        }

        void run() {
            auto bits = 8 + mpz_sizeinbase(*z[i-1], 2);
            if (bits < 512) {
                runner_512.run_test(i, z, result);
            } else if (bits < 1024) {
                runner_1024.run_test(i, z, result);
            } else if (bits < 2048) {
                runner_2048.run_test(i, z, result);
            } else if (bits < 4096) {
                runner_4096.run_test(i, z, result);
            } else {
                printf("Number requires %lu bits, no kernel big enough!\n", bits);
                exit(1);
            }
        }
    private:

        size_t capacity() const {
            return elements;
        }
    private:
        size_t elements;
};



GPUBatch batch(GPU_BATCH_SIZE);
mpz_t start_z;

// This is your setup function
void initialize_module() {
    printf("Setting up gpu_testing.cu\n");
    printf("TESTING PRIMES ON GPU\n");
    printf("PRP/BATCH=%ld\n", GPU_BATCH_SIZE);
    setlocale(LC_NUMERIC, "");

    mpz_init(start_z);
}



int32_t test_gap(uint32_t gap, std::string start, std::vector<uint32_t> offsets) {
    std::vector<uint8_t> result;

    batch.reset();
    mpz_set_str(start_z, start.c_str(), 10);
    uint32_t gpu_i = 0;
    for (auto offset : offsets) {
        batch.active[gpu_i] = true;
        batch.offset[gpu_i] = offset;
        mpz_add_ui(*batch.z[gpu_i], start_z, offset);

        batch.i = ++gpu_i;

        if (batch.i == GPU_BATCH_SIZE) {
            batch.run();
            tests_run += GPU_BATCH_SIZE;

            for (uint32_t j = 0; j < batch.i; j++) {
                auto tmp = batch.offset[j];
                if( batch.result[j] != (tmp == 0 || tmp == gap) ) {
                    printf("ERROR in gap %u at %u prime: %u\n",
                            gap, tmp, batch.result[j]);
                    if (tmp == 0 || tmp == gap) {
                        return -1;
                    }
                    return tmp;
                }
            }
            batch.reset();
            gpu_i = 0;
        }
    }

    if (gpu_i > 0) {
        batch.run();
        tests_run += GPU_BATCH_SIZE;

        for (uint32_t j = 0; j < batch.i; j++) {
            auto tmp = batch.offset[j];
            if( batch.result[j] != (tmp == 0 || tmp == gap) ) {
                printf("ERROR in gap %u at %u prime: %u\n",
                        gap, tmp, batch.result[j]);
                    if (tmp == 0 || tmp == gap) {
                        return -1;
                    }
                    return tmp;
            }
        }
        batch.reset();
    }

    return gap;
}

PYBIND11_MODULE(gpu_testing, m) {
    initialize_module();

    m.doc() = "Test primality of numbers with CGBN miller_rabin";
    m.def("test_gap", &test_gap, "Takes start as a base10 string and offsets to test");
}
