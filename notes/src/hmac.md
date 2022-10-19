# Hash-based Message Authentication Code

Based on [Paul Turner's HMACs video](https://www.youtube.com/watch?v=ODeivrc8Z_g&list=PLDp2gaPHHZK-mnKi3Zy_-hRjqLHh5PaAv&index=11)

- shared key splits into
  - inner key: `xor('5c' * len(shared_key) // 2, shared_key)`
  - outer key: `xor('36' * len(shared_key) // 2, shared_key)`
- `h = Hash(inner_key + msg)`
- `hmac = Hash(outer_key + h)`
- authenticated: `msg + hmac`

## Comparison with Digital Signatures

Digital signatures encrypt message hashes with private key

| | Digital signatures | HMACs |
|:-|:-|:-|
| Pros | No key exchange needed | <ul><li>very fast</li><li>no certificate needed</li></ul> |
| Cons | <ul><li>must get certifcate</li><li>much slower than HMACs</li></ul> | must have secure channel to exchange secret/key |
