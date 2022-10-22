"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
function runServer(handlers) {
    const app = (0, express_1.default)();
    app.use(express_1.default.json());
    app.get("/", (req, res) => {
        res.send(handlers.info());
    });
    app.post("/start", (req, res) => {
        handlers.start(req.body);
        res.send("ok");
    });
    app.post("/move", (req, res) => {
        res.send(handlers.move(req.body));
    });
    app.post("/end", (req, res) => {
        handlers.end(req.body);
        res.send("ok");
    });
    app.use(function (req, res, next) {
        res.set("Server", "battlesnake/github/starter-snake-typescript");
        next();
    });
    const host = '0.0.0.0';
    const port = parseInt(process.env.PORT || '8000');
    app.listen(port, host, () => {
        console.log(`Running Battlesnake at http://${host}:${port}...`);
    });
}
exports.default = runServer;
