# Definitions

Common terms used in cryptography

- **Cryptosystem**
  - defines the key, plaintext, and ciphertext spaces and the encryption/decryption algorithms
  - three spaces
    - `M` = plaintext message space
    - `C` = ciphertext message space
    - `K` = key space
  - two algorithms over these spaces
    - *encryption* `E: M * K -> C`
    - *decryption* `D: C * K -> M`
    - there exist keys `k1` and `k2` such that `D(E(m, k1), k2) == m`

- **Encryption**
  - maps plaintext to ciphertext
  - with a specific cryptosystem in mind, this refers to the encryption algorithm of that system
  - given a plaintext message `m` and key `k`, `c = E(m, k)` is the resulting ciphertext

- **Decryption**
  - maps ciphertext to plaintext
  - with a specific cryptosystem in mind, this refers to the decryption algorithm of that system
  - given a ciphertext message `c` and key `k`, `m = D(c, k)` is the resulting plaintext

- **Symmetric cryptography**
  - same key used for encryption and decryption, i.e. `k1 == k2`

- **Asymmetric cryptography**
  - aka *Public key* cryptography
  - different keys used for encryption and decryption, i.e. `k1 != k2`

- **Confidentiality**
  - ensuring only authorized parties see info
  - achieved via cryptosystems

- **Integrity**
  - detecting when info has been modified/corrupted
  - achieved via [hash functions](./hash_functions.md)

- **Authenticity**
  - verification of the identity of the sender
  - achieved via [digital signatures](./digital_signatures.md)

- **Nonrepudiation**
  - only those with knowledge of the secret can produce a valid signature
  - no forged signatures can exist, unless the secret has been compromised
  - only public

- **Certificates**
  - used to make attestations about public key relationships, typically in the form of a *signature*

- **Hash function**

- **Collision-resistance**

- **Commutative En-/Decryption**
  - ECC is based on commutative algebraic structures
  - multiple key pairs: `(pk1, sk1)`, `(pk2, sk2)`
  - `E(E(m, pk1), pk2) == E(E(m, pk2), pk1)`
  - `D(D(c, sk1), sk2) == D(D(c, sk2), sk1)`
