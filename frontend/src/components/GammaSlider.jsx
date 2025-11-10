import { useState, useEffect } from "react";
import { applyGammaTransform } from "./api";
import "./GammaSlider.css";

export default function GammaSlider() {
  const [config, setConfig] = useState({
    height: 300,
    width: 300,
    gamma: 1,
  });

  const [file, setFile] = useState(null);
  const [image, setImage] = useState(null);

  const handleConfigChange = (e) => {
    const { name, value } = e.target;
    setConfig((oldConfig) => ({
      ...oldConfig,
      [name]: name === "gamma" || name === "height" || name === "width" ? Number(value) : value,
    }));
  };

  const handleFileChange = (e) => {
    const curr = e.target.files[0];
    if (curr) {
      setFile(curr);
      setImage(URL.createObjectURL(curr));
    }
  };

  useEffect(() => {
    if (!file) return;

    const timeout = setTimeout(async () => {
      try {
        const imgUrl = await applyGammaTransform(file, config.gamma);
        if (imgUrl) setImage(imgUrl);
      } catch (err) {
        console.log(`Error at useEffect@GammaSlider.jsx: ${err}`);
      }
    }, 400); // debounce 400ms

    return () => clearTimeout(timeout);
  }, [config.gamma]);

  // Revoke previous blob URL to avoid stale/cached images and memory leaks
  useEffect(() => {
    return () => {
      if (image && typeof image === "string" && image.startsWith("blob:")) {
        try { URL.revokeObjectURL(image); } catch (_) {}
      }
    };
  }, [image]);

  const openFileDialog = () => {
    document.getElementById("photo").click();
  };

  return (
    <>
      <div className="GammaSlider">
        <div className="left-pane">
          <div className="photo-container">
            {image ? (
              <img
                src={image}
                alt="preview"
                height={config.height}
                width={config.width}
              />
            ) : (
              <span>No image loaded</span>
            )}
            <input
              id="photo"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </div>
          <button onClick={openFileDialog}>Load</button>
        </div>

        <div className="right-pane">
          <label htmlFor="height">Height</label>
          <input
            id="height"
            type="number"
            placeholder="height"
            value={config.height}
            name="height"
            onChange={handleConfigChange}
          />
          <label htmlFor="width">Width</label>
          <input
            id="width"
            type="number"
            placeholder="width"
            value={config.width}
            name="width"
            onChange={handleConfigChange}
          />
          <label htmlFor="gamma">Gamma</label>
          <input
            id="gamma"
            type="range"
            min="0.1"
            max="3"
            step="0.1"
            value={config.gamma}
            name="gamma"
            onChange={handleConfigChange}
          />
          <span>{config.gamma}</span>
        </div>
      </div>
    </>
  );
}
