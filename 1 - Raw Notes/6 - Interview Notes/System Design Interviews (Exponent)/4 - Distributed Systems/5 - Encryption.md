Date: 2026-02-16
Course: https://www.tryexponent.com/courses/system-design-interviews/encryption
Tags: [[System Design Interview]] [[Distributed System]] [[5 - Encryption]]

# Content

Cryptography is the study of encrypting and decrypting information for secure transmission between two parties. Generally, there are two steps:

- **Encryption** is the process of converting plain text into code, or **ciphertext.**
- **Decryption** is the reverse - converting ciphertext back to **plaintext**.

## Why encryption matters[](https://www.tryexponent.com/courses/system-design-interviews/encryption#why-encryption-matters)

At a high level, businesses have three powerful tools to help keep both user data and internal data out of the wrong hands. These are **encryption**, **authentication**, and **authorization** (the latter two will be covered in the next lesson.)

> **Note:** Given the tradeoff between _security_ and _user experience_, tools which are more or less invisible to users are ideal.

Encryption is a perfect example of a non-intrusive security measure.

## How it works[](https://www.tryexponent.com/courses/system-design-interviews/encryption#how-it-works)

Generally, an encryption algorithm translates (encodes) plaintext into ciphertext, making it unreadable and therefore useless to anyone without the **decryption key**. There are two basic types of encryption.

### Symmetric encryption

Symmetric encryption uses the _same_ key for both encryption and decryption. It's fast and easy, provided that the key stays secret.
![](assets/5%20-%20Encryption/file-20260216232820416.png)

This might sound risky, but it isn't provided that you follow a few guidelines. The strength of the key depends on:

- Its length
- Its entropy (or, the "randomness" inherent in creating it)
- How easy it is to deconstruct

Symmetric algorithms (or ciphers) take one of two forms: block or stream. **Block ciphers** encrypt data in blocks, where **stream ciphers** encrypt data one bit at a time. **AES**, or the **Advanced Encryption Standard** is a block cipher used across the internet. Key lengths range from 128 to 256-bits, which is quite long. AES using a 256-bit key is considered unbreakable.

### Asymmetric encryption

Asymmetric encryption uses two different keys for encryption and decryption. The encryption (public) key is visible to all, while the decryption key stays private. Asymmetric encryption takes longer, but it's considered to be more secure.
![](assets/5%20-%20Encryption/file-20260216232832722.png)
Some well-known examples of asymmetric encryption algorithms include **RSA** ([RSA stands for Ron Rivest, Adi Shamir, and Leonard Adleman— the men who first publicly described the algorithm in 1977](https://www.digicert.com/faq/cryptography/what-is-rsa-cryptography)), which was developed alongside early **TLS (Transport Layer Security).** While RSA is considered less robust than **Diffie-Hellman Key Exchange**, Diffie-Hellman doesn't authenticate and RSA does. Both use mathematics to generate decryption keys that are all but impossible for attackers to deconstruct, and both are used extensively today.


## Symmetric and asymmetric encryption work together in SSL/TLS[](https://www.tryexponent.com/courses/system-design-interviews/encryption#symmetric-and-asymmetric-encryption-work-together-in-ssl-tls)

Symmetric encryption is considered less secure than asymmetric, but it's faster and uses less computing power. To provide security over a network, these two methods are used in tandem.

**SSL (Secure Sockets Layer)** is an older form of **TLS (Transport Layer Security),** a protocol running on the application layer of the Internet that's designed to secure web communications through a **TLS handshake.** To establish a TLS connection, the client can either:

- Make a request using port 443 (reserved for encrypted HTTPS traffic), or
- Request that the server switch to TLS. If the server agrees, a handshake is initiated.

An asymmetric cipher generates a session-specific shared key while further communication is symmetrically encrypted. The overall connection is protected with the more secure asymmetric cipher, but beneath that, symmetric encryption is used to protect the data without slowing down transmission.

## Password protection with bcrypt[](https://www.tryexponent.com/courses/system-design-interviews/encryption#password-protection-with-bcrypt)

Data transmitted over TLS is considered safe, but what about sensitive data stored in a database, like user passwords? Generally, the best practice is to **hash** and **salt** passwords using a powerful, time-tested algorithm like **bcrypt.** Hashing mathematically scrambles the data, making it difficult to reverse-engineer. But since passwords are _short_ and can be _predictable -_ like "MyPassword", hashed passwords may still be susceptible to brute-force attacks. Salting helps address both of these by adding a unique value to the end of a password before hashing. This makes it longer and increases entropy. Bcrypt, which has been around for decades, hashes and salts passwords in a way that slows down brute force attacks even as computing power increases. Even though it's old by some standards, it's considered industry-grade and plenty of popular authentication & authorization platforms depend on it to protect passwords.

> **Tip:** Don't confuse encryption with hashing. Using bcrypt (or similar methods) _irreversibly_ hashes (scrambles) the password so that it isn't stored anywhere. Even those with direct database access can't see them.

## When to bring up encryption in an interview[](https://www.tryexponent.com/courses/system-design-interviews/encryption#when-to-bring-up-encryption-in-an-interview)

It's unlikely you'll have to go into detail, but it's good to know best practices for encryption. Generally, you should encrypt both **in transit** and **at rest**. Encrypting in transit these days mainly means using HTTPS rather than HTTP, making use of TLS protocols above.

Encrypting at rest means protecting data while in storage. Most modern databases allow for encryption, often AES 256-bit. The best practice for password protection is to both hash and salt passwords using something like bcrypt.

Depending on your application, you may also want to encrypt while processing (for example, if you're working in fintech.) Cloud architecture offers great options.

Finally, modern messaging apps like iMessage, Whatsapp, and Signal often use **end-to-end encryption (E2EE)**. In these, the message is actually encrypted from one user to another, so the unencrypted message is never stored anywhere except on the user's device.
# Note


# Reference

