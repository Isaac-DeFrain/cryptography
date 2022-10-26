# Lattice-based Crypto

[Chris Peikert](https://www.youtube.com/watch?v=FVFw_qb1ZkY)

## Hard problems

### Short Integer Solution (SIS) problem

Find  `z \in {-1, 0, 1}^m` such that

```
Az = 0 in (ℤ/qℤ)^n
```

#### Collision-resistant hash function

```
A \in {0, 1}^m -> (ℤ/qℤ)^n
f(x) = Ax
```

#### Digital signatures

- generate uniform `vk = A` with secret *trapdoor* `sk = T`
- `Sign(T, msg)` use `T` to sample a short `z \in Z^m` such that `Az = H(msg) \in (Z/qZ)^n` using discrete Gaussian distribution
- `Verify(A, msg, z)` check that `Az = H(msg)` and `z` is sufficiently short
- Security: forging a signature for a new message `msg*`requires finding a short `z* \in Z^m` such that `Az* = H(msg*)` (this is the SIS problem!)

### Learning with errors (LWE)

Find secret `s \in (ℤ/qℤ)^n` given many 'noisy' inner products

LWE is versatile

Kinds of crypto LWE can do

- [x] key exchange, private key encryption
- [x] oblivious transfer (MPCs)
- [x] actively secure encrytion (w/o random oracles)
- [x] block ciphers, PRFs

-------

- [x] Identity-bsed encryption (w/o RO)
- [x] hierarchical ID-based encryption (w/o RO)

-------

- [ ] fully homorphic encryption
- [ ] attrbute-based encryption for arbitrary policies
- [ ] much more!

#### Key exchange with LWE

```
    Alice                        Bob
  r <- ℤ^m                     s <- ℤ^m
  u ~ r^t A --------------------->
      <------------------------ v ~ As
  r^tv ~ r^t As               us ~ r^t As
```

### Polynomial rings

TODO
