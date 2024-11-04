const { poseidon2 } = require('poseidon-lite')

class MerkleTree {
    constructor(data) {
        this.leaves = data;
        this.levels = [this.leaves];
        this.buildTree();
    }

    hash(left,right) {
        return poseidon2([left, right])
    }
    buildTree() {
        let currentLevel = this.leaves;

        while (currentLevel.length > 1) {
            currentLevel = this.createParentLevel(currentLevel);
            this.levels.push(currentLevel);
        }
    }

    createParentLevel(currentLevel) {
        const parentLevel = [];

        for (let i = 0; i < currentLevel.length; i += 2) {
            const left = currentLevel[i];
            const right = currentLevel[i + 1] || currentLevel[i];
            const parentHash = this.hash(left , right);
            parentLevel.push(parentHash);
        }

        return parentLevel;
    }

    getLevelWithNodeCount(count) {
        for (let i = 0; i < this.levels.length; i++) {
            if (this.levels[i].length === count) {
                return { levelIndex: i, nodes: this.levels[i] };
            }
        }
        return null; // Return null if no such level exists
    }

    getRoot() {
        return this.levels[this.levels.length - 1][0];
    }

    getLeaves() {
        return this.leaves;
    }

    getLevels() {
        return this.levels;
    }
}

let data = [];
for (let index = 0; index <1200; index++) {
    data.push(index)
}
const merkleTree = new MerkleTree(data);
console.log("Merkle Root:", merkleTree.getRoot());
console.log(merkleTree.getLevelWithNodeCount(8))