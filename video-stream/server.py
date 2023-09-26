import cv2
import asyncio
import aiortc
from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer

class VideoTransformTrack(MediaStreamTrack):
    def __init__(self, track):
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        # Faça qualquer processamento de quadros aqui (opcional)
        return frame

async def run(pc, player, signaling):
    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("iceconnectionstatechange")
    def on_iceconnectionstatechange():
        print("ICE connection state is", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            pc.close()

    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

    for track in player.audio_tracks + player.video_tracks:
        pc.addTrack(track)

    await signaling.connect()

if __name__ == "__main__":
    player = MediaPlayer("/path/to/your/video.mp4")

    pc = aiortc.RTCPeerConnection()
    signaling = WebsocketSignaling("ws://localhost:8080")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(pc, player, signaling))
    loop.run_forever()
