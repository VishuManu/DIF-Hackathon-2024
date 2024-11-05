## Inspiration
The primary motivation behind creating this proof of concept is to demonstrate how Zero-Knowledge Proofs (ZKPs) and Verifiable Credentials (VCs), aligned with W3C standards, can be integrated with on-chain blockchain technology i.e (CHEQD). This approach enables the deployment, storage, and verification of proof of human identity—an essential capability as we approach an AI-driven era where distinguishing between real users and bots or AI agents will become increasingly challenging. Without effective solutions to authenticate human identity, the risk of misuse could be significant.



## What it does
1.**Government ID Issuance:** A government agency issues an ID to the holder, which is required to obtain a PHC Verifiable Credential (VC).

2.**Presenting ID to PHC Provider:** The holder presents their government-issued VC from their wallet to the PHC provider, a trusted authority.

3.**Fingerprint Biometric Capture:** Once the government ID is verified, the user scans their fingerprint using PHC’s biometric infrastructure, which extracts unique fingerprint features.

4.**Merkle Tree and ZKP Generation:** The PHC provider encodes fingerprint data into a Merkle tree (due to its unique X/Y axis and orientation features), stores the Merkle root hash on the credential, and generates a ZKP circuit.

5.**Credential Issuance:** The holder receives the PHC credential, ZKP proving key, signed verification key, and raw fingerprint data over a **_DIDComm v2 channel._**

6.**Online Authentication :** When accessing an online service that requires PHC verification, the user shares the PHC credential from their wallet with the service.

7.**Verification Process:** The service provider’s DIDComm v2 agent performs ZKP verification with the holder’s data. If verified, access is granted; otherwise, it is denied.

8. **Monetization** :While not yet practically implemented, we also discuss how, in the future, issuers of PHC could take advantage of issuing PHC as an initiative based on their biometric infrastructure.in the form of **CHEQD** Token

![_](https://i.imgur.com/WCzMso8.png)

## How we built it
1. This Whole Frontend is made on Typescript,Tailwind css
2. The [DIDCOMMv2](https://identity.foundation/didcomm-messaging/spec/) agent is made upon on solely python in which the exchange of dicomm message happen between verifier/issuer and holder
3. [DID:PEER](https://identity.foundation/peer-did-method-spec/) Protocol and creation is made on Python as well
4. We use did universal resolver/registrar by universal decneterlized identity for CHEQD for deploying and registering the did on chain basically for [testing on testnet of cheqd](https://testnet-faucet.cheqd.io/)
5. Whole ZPK Circuit for proof generation and verification is developed using [circom](https://docs.circom.io/circom-language/signals/) ZK language and proof is also created using circom compiler.

This is sample code image that represent how custom circom ZKP language looks like that help us to generate proof:

![Code Snippet](https://i.imgur.com/7CMbPKR.png)

## Challenges we ran into
1. **Poseidon Hash:** One of the major challenges we face is using [Poseidon hash](https://www.poseidon-hash.info/ ) instead of SHA-256. In Zero-Knowledge Proofs (ZKP), it’s recommended to use Poseidon over SHA-256, as creating a [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) with Poseidon hash is more efficient. Learning about this aspect has been quite challenging.

2. **Circom ZKP Language:** The second challenge we face is understanding the Circom ZKP language and learning how to write a ZKP circuit, as well as compiling it using the built-in compiler written in Rust.



## Accomplishments that we're proud of
One of our biggest accomplishments has been implementing an advanced Zero-Knowledge Proof (ZKP) using circuits. Previously, most Verifiable Credentials (VCs) implemented ZKP in the **BBS** format, but we achieved this through our [SD-JWT format Envelop Format](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-credential-that-uses-an-enveloping-proof-in-sd-jwt-format) On top of that, we integrated circuit-based proofs into our credentials, making them more advanced and unlocking additional use cases.and verifying the biometric merkel hash is not a feasiable task by BBS. thats why we tries to explore it using circuit based ZKP that operate on agents machine _(insipred from ACA-PY)_

## What I learned
1. **Learning ZKP Mechanics:** First, I studied how Zero-Knowledge Proofs (ZKPs) are generated and verified.

2. **Mastering DIDComm v2:** Next, I focused on the DIDComm v2 messaging protocol, which is crucial for securely transmitting confidential ZKP proof data alongside credentials.

3. **Exploring DID Protocol:**Finally, I learned about DID Peer and DID Test. The DID key method is important for the holder, as it is a 'subject DID' method that incurs no transaction costs—similar to DID Peer in terms of cost efficiency. I also explored how this protocol differs from public blockchains, particularly in managing private and secure connections.


## What's next for Decentralized PHC Credentials in the Future AI Era
1. **Monetization:** In the future, we plan to create monetization opportunities, allowing verifiers to pay issuers a certain amount of ```CHEQD``` tokens to support the initiative of setting up the necessary infrastructure.

2. **Expanded Cryptography Support:** Currently, we support only 1-2 elliptic curves, as we’re primarily demonstrating proof of concept. We use Ed25519, which is also used in the creation of the ```did:cheqd:testnet``` DID method, hosted on the Cheqd testnet.

3. **Refining DIDComm v2:** Enhancing security is a priority, so we plan to implement additional endpoints and protocols, such as trust ping, to strengthen security and reliability.

4. **Scaling ZKP:** We’re also working on making the ZKP implementation with Circom more reliable, faster, and scalable by utilizing the same DIDComm protocol.

5. **Creating More Secure Wallet**:Currently for Proof of concept demonstration we use simple storing of keys , but in future we implment KERI managemen tof keys and creating Rust wallet for more security on system level also 
