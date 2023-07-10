#include "benchmark/benchmark.h"

#define BASIC_BENCHMARK_TEST(x) BENCHMARK(x)->Arg(8)->Arg(512)->Arg(8192)

void BM_empty(benchmark::State& state)
{
    for (auto _ : state)
    {
        auto iterations = state.iterations();
        benchmark::DoNotOptimize(iterations);
    }
}
BENCHMARK(BM_empty);
BENCHMARK(BM_empty)->ThreadPerCpu();

void BM_spin_empty(benchmark::State& state)
{
    for (auto _ : state)
    {
        for (auto x = 0; x < state.range(0); ++x)
        {
            benchmark::DoNotOptimize(x);
        }
    }
}
BASIC_BENCHMARK_TEST(BM_spin_empty);
BASIC_BENCHMARK_TEST(BM_spin_empty)->ThreadPerCpu();

void BM_spin_pause_before(benchmark::State& state)
{
    for (auto i = 0; i < state.range(0); ++i)
    {
        benchmark::DoNotOptimize(i);
    }
    for (auto _ : state)
    {
        for (auto i = 0; i < state.range(0); ++i)
        {
            benchmark::DoNotOptimize(i);
        }
    }
}
BASIC_BENCHMARK_TEST(BM_spin_pause_before);
BASIC_BENCHMARK_TEST(BM_spin_pause_before)->ThreadPerCpu();

// Ensure that StateIterator provides all the necessary typedefs required to
// instantiate std::iterator_traits.
static_assert(
    std::is_same<typename std::iterator_traits<
                     benchmark::State::StateIterator>::value_type,
                 typename benchmark::State::StateIterator::value_type>::value,
    "");

BENCHMARK_MAIN();
