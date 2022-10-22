"use strict";
// Welcome to
// __________         __    __  .__                               __
// \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
//  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
//  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
//  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
//
// This file can be a nice home for your Battlesnake logic and helper functions.
//
// To get you started we've included code to prevent your Battlesnake from moving backwards.
// For more info see docs.battlesnake.com
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const server_1 = __importDefault(require("./server"));
let lastMove = "";
// info is called when you create your Battlesnake on play.battlesnake.com
// and controls your Battlesnake's appearance
// TIP: If you open your Battlesnake URL in a browser you should see this data
function info() {
    console.log("INFO");
    return {
        apiversion: "1",
        author: "st3rbini",
        color: "#b56c0d",
        head: "tiger-king",
        tail: "tiger-tail", // TODO: Choose tail
    };
}
// start is called when your Battlesnake begins a game
function start(gameState) {
    console.log("GAME START");
}
// end is called when your Battlesnake finishes a game
function end(gameState) {
    console.log("GAME OVER\n");
}
function getNumberOfMoves(isMoveSafe) {
    return Number(isMoveSafe.up) + Number(isMoveSafe.left) + Number(isMoveSafe.down) + Number(isMoveSafe.right);
}
// move is called on every turn and returns your next move
// Valid moves are "up", "down", "left", or "right"
// See https://docs.battlesnake.com/api/example-move for available data
function move(gameState) {
    let isMoveSafe = {
        up: true,
        down: true,
        left: true,
        right: true
    };
    // We've included code to prevent your Battlesnake from moving backwards
    const myHead = gameState.you.body[0];
    const myNeck = gameState.you.body[1];
    const myTail = gameState.you.body[gameState.you.body.length - 1];
    if (myNeck.x < myHead.x) { // Neck is left of head, don't move left
        isMoveSafe.left = false;
    }
    else if (myNeck.x > myHead.x) { // Neck is right of head, don't move right
        isMoveSafe.right = false;
    }
    else if (myNeck.y < myHead.y) { // Neck is below head, don't move down
        isMoveSafe.down = false;
    }
    else if (myNeck.y > myHead.y) { // Neck is above head, don't move up
        isMoveSafe.up = false;
    }
    // Disable moves against boundaries
    if (myHead.y + 1 === gameState.board.height)
        isMoveSafe.up = false;
    if (myHead.y - 1 < 0)
        isMoveSafe.down = false;
    if (myHead.x + 1 === gameState.board.width)
        isMoveSafe.right = false;
    if (myHead.x - 1 < 0)
        isMoveSafe.left = false;
    // Disable moves against its own body
    gameState.you.body.forEach(particle => {
        // Stessa Y 
        if (myHead.y === particle.y) {
            // Obstacle on left 
            if (particle.x === myHead.x - 1)
                isMoveSafe.left = false;
            // Obstacle on right
            if (particle.x === myHead.x + 1)
                isMoveSafe.right = false;
        }
        // Stessa X
        if (myHead.x === particle.x) {
            // Obstacle on up
            if (particle.y === myHead.y + 1)
                isMoveSafe.up = false;
            // Obstacle on down
            if (particle.y === myHead.y - 1)
                isMoveSafe.down = false;
        }
    });
    console.log(gameState);
    // TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    // myBody = gameState.you.body;
    // TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    // opponents = gameState.board.snakes;
    // Are there any safe moves left?
    const safeMoves = Object.keys(isMoveSafe).filter((key) => isMoveSafe[key]);
    /*
    if(safeMoves.length > 1) {
      // Pick the move that takes the snake far away from the tail
      safeMoves.filter(move => {
        return (move === 'down' && myTail.y > myHead.y) ||
          (move === 'up' && myTail.y < myHead.y) ||
          (move === 'left' && myTail.x > myHead.x) ||
          (move === 'right' && myTail.x < myHead.x);
      });
    }  */
    // TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    // food = gameState.board.food;
    let nextMove = "down";
    if (safeMoves.length > 0) {
        nextMove = safeMoves[Math.floor(Math.random() * safeMoves.length)];
    }
    console.log(`MOVE ${gameState.turn}: ${nextMove}`);
    lastMove = nextMove;
    return { move: nextMove };
}
(0, server_1.default)({
    info: info,
    start: start,
    move: move,
    end: end
});
