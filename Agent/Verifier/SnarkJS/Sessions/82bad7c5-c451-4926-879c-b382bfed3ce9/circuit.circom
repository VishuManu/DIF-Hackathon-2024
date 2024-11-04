pragma circom 2.0.0;

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

component main  = MerkleTree(3);