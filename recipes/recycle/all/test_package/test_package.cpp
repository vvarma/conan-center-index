#include <cassert>
#include <recycle/shared_pool.hpp>

struct heavy_object {};

int main() {
  recycle::shared_pool<heavy_object> pool;
  // Initially the pool is empty
  assert(pool.unused_resources() == 0U);
  { auto o1 = pool.allocate(); }
  // Heavy object is back in the pool
  assert(pool.unused_resources() == 1U);
}