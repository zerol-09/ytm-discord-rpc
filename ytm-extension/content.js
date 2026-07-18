console.log("[YTMusic RPC] loaded");

let lastId = null;

const script = document.createElement("script");
script.src = chrome.runtime.getURL("injected.js");

(document.head || document.documentElement).appendChild(script);

script.onload = () => {
    script.remove();
};


window.addEventListener("message", (event) => {
    if (event.data.type === "YT_VIDEO_ID") {
        lastId = event.data.id;
    }
});



let lastsong = "";
let lasttime = 0;
let last_position = -1;
let drift_threshold = 2;

function getSongData() {
  const time = Date.now();
  const titleEl = document.querySelector(
    'ytmusic-player-bar yt-formatted-string.title[title]'
  );

  const artistEl = document.querySelector(
    'ytmusic-player-bar .byline'
  );

  const thumbnailEl = document.querySelector(
    'ytmusic-player-bar img'
  );
  
  const timeinfoEl = document.querySelector(
    'ytmusic-player-bar .time-info'
  );

  const playerstateEl = document.querySelector(
    'ytmusic-player-bar .play-pause-button'
  );

  const durationMin = timeinfoEl?.textContent?.split("/")[1]?.trim();
  const [min, sec] = durationMin ? durationMin.split(":").map(Number) : [0, 0];

  const positionMin = timeinfoEl?.textContent?.split("/")[0]?.trim();
  const [posMin, posSec] = positionMin ? positionMin.split(":").map(Number) : [0, 0];

  const thumbnailSmall = thumbnailEl?.getAttribute("src") || "";

  const artistText = artistEl?.getAttribute("title") || "";

  const title = titleEl?.getAttribute("title") || null;
  const artist = artistText ? artistText.split("•")[0].trim() : null;
  const thumbnail = thumbnailSmall?.replace(/=w\d+-h\d+-l\d+-rj/, "=w500-h500-l90-rj");
  const duration = min * 60 + sec;
  const position = posMin * 60 + posSec;
  const isPlaying = playerstateEl?.getAttribute("title") === "Pause";
  
  return { title, artist, thumbnail, duration, position, isPlaying, time };
}



function senddata() {

    let { title, artist, thumbnail, duration, position, isPlaying, time } = getSongData();
    if (!title && !artist && !thumbnail && duration && lasttime === 0){
      lasttime=time;
      return;
    }
    if (lasttime !==0){
      time = lasttime;
      lasttime=0;
    }
    const new_song = lastId !== lastsong.lastId
    if (new_song){
      last_position=-1;
    }
    const time_drifted = Math.abs((position - last_position) - 1) > drift_threshold && last_position >= 0;
    last_position = position;
    if (!title || !artist || !thumbnail || !lastId) return;
    if ( title === lastsong.title && artist === lastsong.artist && thumbnail === lastsong.thumbnail && isPlaying === lastsong.isPlaying && !time_drifted ) return;
    
    lastsong = { lastId, title, artist, thumbnail, isPlaying };
    
    console.log("Sending song data:", lastId, title, artist, thumbnail, duration, position, isPlaying, time);
    fetch("http://127.0.0.1:5000/song", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: `https://music.youtube.com/watch?v=${lastId}`,
            title: title,
            artist: artist,
            thumbnail: thumbnail,
            duration: duration,
            position: position,
            isPlaying: isPlaying,
            time: time
        })
    })
    .then(() => console.log("Sent song data:", lastId, title, artist, thumbnail, duration, position, isPlaying, time))
    .catch(err => console.error("FETCH ERROR:", err));
    
}

setInterval(senddata,500)