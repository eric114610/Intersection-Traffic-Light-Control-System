// import ReactPlayer from 'react-player';
// import {useState} from 'react';
import './VideoBackground.css'
const VideoBackground = () => {
    // 指定您的视频文件的路径
    const videoSource = `${process.env.PUBLIC_URL}/Bg.mp4`; // 更改为您的视频文件的实际路径

    return (
      <div className="video-background">
        <video autoPlay muted loop>
          <source src={videoSource} type="video/mp4" />
          您的浏览器不支持视频标签
        </video>
      </div>
    );
  };
export default VideoBackground;