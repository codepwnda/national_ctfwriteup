#include <stdio.h>
#include <stdint.h>
#include <limits.h>

const int flag[] = {0xB0BECABE, 0xBCBECAFE, 0xB73ECAFE, 0xB73ECAFE, 0xB7BECADE, 0xB73ECABE, 0xB63ECA9E, 0xB13ECA9E, 0xB4BECABE, 0xB33ECA9E, 0xB4BECABE, 0xB0BECABE, 0xB3BECADE, 0xB73ECABE, 0xBC3ECABE, 0xB13ECA9E, 0xBC3ECA9E, 0xB3BECAFE, 0xBCBECA9E, 0xB13ECA9E, 0xB6BECABE, 0xBCBECADE, 0xB43ECAFE, 0xBC3ECADE};

uint32_t rotl32 (uint32_t value, unsigned int count) {
    const unsigned int mask = CHAR_BIT * sizeof(value) - 1;
    count &= mask;
    return (value << count) | (value >> (-count & mask));
}

uint32_t rotr32 (uint32_t value, unsigned int count) {
    const unsigned int mask = CHAR_BIT * sizeof(value) - 1;
    count &= mask;
    return (value >> count) | (value << (-count & mask));
}

uint16_t rotr16 (uint16_t value, unsigned int count) {
    const unsigned int mask = CHAR_BIT * sizeof(value) - 1;
    count &= mask;
    return (value >> count) | (value << (-count & mask));
}

uint16_t rotl16 (uint16_t value, unsigned int count) {
    const unsigned int mask = CHAR_BIT * sizeof(value) - 1;
    count &= mask;
    return (value << count) | (value >> (-count & mask));
}

int main(int argc, char const *argv[])
{
  int tmp = 0 ;
  char f[24] = { 0 };

  for (int i = 0; i < 24; ++i) {
    tmp = flag[i] ^ 0xbabecafe;
    tmp = rotl32(tmp, 9);
    tmp = rotr16(tmp, 11);
    tmp = rotr32(tmp, 26);
    tmp = rotl16(tmp, 7);
    f[i] = tmp;
  }

  printf("JOINTS19{%s}\n", f);
  return 0;
}