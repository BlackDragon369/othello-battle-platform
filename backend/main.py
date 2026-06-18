# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from othello_core import *

app = FastAPI(title="Othello 联机对战服务")
# 跨域：允许GitHub Pages前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 房间存储 {room_id: {"players": [ws1, ws2], "board": board, "turn": BLACK}}
rooms = {}

def broadcast(room_id: str, data: dict):
    """房间内全员广播消息"""
    if room_id not in rooms:
        return
    msg = json.dumps(data)
    for ws in rooms[room_id]["players"]:
        try:
            await ws.send_text(msg)
        except:
            pass

@app.websocket("/ws/{room_id}")
async def ws_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    # 初始化房间
    if room_id not in rooms:
        rooms[room_id] = {
            "players": [],
            "board": init_board(),
            "turn": BLACK
        }
    room = rooms[room_id]
    # 最多2人对局
    if len(room["players"]) >= 2:
        await websocket.send_text(json.dumps({"type":"full","msg":"房间已满"}))
        await websocket.close()
        return
    room["players"].append(websocket)
    try:
        # 通知房间人数更新
        await broadcast(room_id, {
            "type":"room_info",
            "count": len(room["players"]),
            "board": board_to_json(room["board"]),
            "turn": room["turn"]
        })
        # 主消息循环
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            if data["type"] == "move":
                r, c = data["r"], data["c"]
                current_board = json_to_board(data["board"])
                current_player = data["player"]
                # 校验落子合法性
                if can_place(current_board, r, c, current_player) and current_player == room["turn"]:
                    place_piece(current_board, r, c, current_player)
                    room["board"] = current_board
                    # 切换回合
                    next_p = WHITE if current_player == BLACK else BLACK
                    # 判断下家有无可走棋，无则自动跳过
                    if not get_all_valid_moves(current_board, next_p):
                        next_p = BLACK if next_p == WHITE else WHITE
                    room["turn"] = next_p
                    # 判断游戏结束
                    over = game_over(current_board)
                    score_b, score_w = count_score(current_board)
                    # 广播对局最新状态
                    await broadcast(room_id, {
                        "type":"update",
                        "board": board_to_json(current_board),
                        "turn": room["turn"],
                        "game_over": over,
                        "score_black": score_b,
                        "score_white": score_w
                    })
    except WebSocketDisconnect:
        room["players"].remove(websocket)
        if len(room["players"]) == 0:
            del rooms[room_id]
        else:
            await broadcast(room_id, {"type":"leave","msg":"玩家离线"})