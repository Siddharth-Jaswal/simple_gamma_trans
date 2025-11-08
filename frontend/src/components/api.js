import axios from "axios";

const url = "http://localhost:5000/api/gamma-transform";

export async function applyGammaTransform(file, gamma) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("gamma", gamma);

  try {
    const res = await axios.post(url, formData, {
      responseType: "blob",
    });
    return URL.createObjectURL(res.data);
  } catch (err) {
    console.error(`Error at applyGammaTransform@api.js: ${err.message}`);
  }
}
