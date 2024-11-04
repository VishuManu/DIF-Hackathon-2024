const express = require('express');
const bodyParser = require('body-parser');
const snarkjs = require('snarkjs');
const path = require('path');
const { exec } = require("child_process");
const fs = require('fs');
const { time } = require('console');
const app = express();
const PORT = process.env.PORT || 5010;
const { spawn } = require('child_process');
const { stdout, stderr, cwd } = require('process');
const crypto = require('crypto');

app.use(bodyParser.json());


// This server can be operated either by the issuer if they have the required expertise,
// or by the protocol or ZK Proof developer, or a third-party service facilitating this functionality.
// Ultimately, the verifier needs to place their trust in one entity as the central authority:
// either the issuer, the protocol developer, or a trusted service provider.

app.post("/execute_circuit", (req, res) => {
    const _data = req.body
    const d = create_circuit(_data["session"], "digest_pre_image_proof", _data["_16nodes_biometrics_merkel"])
    return res.status(200).send("Done")
})
app.post("/verify", (req, res) => {
    const data = req.body
    exec("ls",{cwd:data["cwd"]},(error,stdout,stderr)=>{
        if(!error)
            console.log(error)
        console.log(stdout)
    })

    return res.status(200).send("Done")
})
function file_format() {
    const circuit = `pragma circom 2.0.0;

include "../../circomlib/circuits/poseidon.circom";

template HashLeftRight() {
    signal input left;
    signal input right;
    signal output hash;
    component poseidon = Poseidon(2);

    poseidon.inputs[0] <== left;
    poseidon.inputs[1] <== right;
    hash <== poseidon.out;
}

template MerkleTreeLevel(leafCount, nodeCount) {
    signal input leaves[leafCount];
    signal output nodes[nodeCount];

    leafCount === 2*nodeCount;

    component hashers[nodeCount];

    var i = 0;
    var n = 0;
    while(i < nodeCount){
    hashers[i] = HashLeftRight();
    hashers[i].left <== leaves[n]; 
    hashers[i].right <== leaves[n + 1];
    nodes[i] <== hashers[i].hash;


    i++;
    n+=2;
    }
}

template MerkleTree(levels){
    signal input leaves[2**levels];
    signal output root;

    component merkleLevels[levels]; 

    var i = 0;
    while(i < levels){
        var leafCount = 2**(levels - i);
        var nodeCount = 2**(levels - i - 1);

        merkleLevels[i] = MerkleTreeLevel(leafCount, nodeCount); 
    
        var n = 0;
        while(n < leafCount){
            merkleLevels[i].leaves[n] <== i == 0 ? leaves[n] : merkleLevels[i - 1].nodes[n];

            n++;
        }

        
        i++;
    }

    root <== merkleLevels[levels - 1].nodes[0];
}

component main  = MerkleTree(3);`

    return circuit;

}
async function create_circuit(session_id, zkp_type, _16nodes_biometrics_merkel) {
    const _path = path.join(__dirname, "Sessions", session_id)
    const circuit_name = "circuit.circom"
    if (!fs.existsSync(_path))
        fs.mkdirSync(_path, { recursive: true })
    console.log("Session Created")


    if (zkp_type == "digest_pre_image_proof")
        fs.writeFileSync(path.join(_path, circuit_name), file_format())


    exec(`circom ${circuit_name} --r1cs --wasm --sym  -l ../../circomlib/`, { cwd: _path }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error output: ${stderr}`);
            return;
        }

        console.log(`Command output: ${stdout}`);
        phase2(_path, "circuit", _16nodes_biometrics_merkel)
    })

}
async function phase2(cwd, circuit_name, _16nodes_biometrics_merkel) {
    exec("snarkjs powersoftau new bn128 12 pot12_0000.ptau -v", { cwd: cwd }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error output: ${stderr}`);
            return;
        }

        console.log(`Command output: ${stdout}`);
        const step2 = snarkjs.powersOfTau.contribute(path.join(cwd, "pot12_0000.ptau"), path.join(cwd, "pot12_0001.ptau"), "test", "test")
        step2.then((_) => {
            const prepare = snarkjs.powersOfTau.preparePhase2(path.join(cwd, "pot12_0001.ptau"), path.join(cwd, "pot12_final.ptau"))
            prepare.then((_) => {
                const _key = snarkjs.zKey.newZKey(path.join(cwd, `${circuit_name}.r1cs`), path.join(cwd, "pot12_final.ptau"), path.join(cwd, "multiplier2_0000.zkey"))
                _key.then(() => {
                    const _key_contribute = snarkjs.zKey.contribute(path.join(cwd, "multiplier2_0000.zkey"), path.join(cwd, "multiplier2_0001.zkey"), "Test", "test")
                    console.log("hhh")
                    exec(`snarkjs zkey export verificationkey multiplier2_0001.zkey verification_key.json`, { cwd: cwd }, (error, stdout, stderr) => {
                        calculateWitness(cwd, _16nodes_biometrics_merkel)


                    })

                })

            })

        }).catch((reason) => {
            console.log(reason)
        })
    })

}
function calculateWitness(_path, _16nodes_biometrics_merkel) {

    const inputs = {
        "leaves": _16nodes_biometrics_merkel
    };
    console.log("Calculating witness...");
    const witness = snarkjs.wtns.calculate(inputs, path.join(_path, "circuit_js/circuit.wasm"), path.join(_path, "t.wtns"));
    witness.then((_) => {
        exec(`snarkjs groth16 prove multiplier2_0001.zkey t.wtns proof.json public.json`, { cwd: _path }, (error, stdout, stderr) => {
            if (error)
                console.log(error.message)
            console.log("Done")
        })
    })

}

app.listen(PORT, () => {
    console.log("Listening....")
})
//const hash = 
//console.log(hash.toString())

