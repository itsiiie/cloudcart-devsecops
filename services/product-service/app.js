const express = require("express");
const redis = require("redis");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const redisClient = redis.createClient({
  url: "redis://redis:6379",
});

redisClient.connect();

const products = [
  { id: 1, name: "Laptop", price: 1000 },
  { id: 2, name: "Phone", price: 500 },
  { id: 3, name: "Headphones", price: 100 },
];

app.get("/", (req, res) => {
  res.json({ message: "Product service running" });
});

app.get("/products", async (req, res) => {
  const cache = await redisClient.get("products");

  if (cache) {
    return res.json(JSON.parse(cache));
  }

  await redisClient.set("products", JSON.stringify(products), {
    EX: 60,
  });

  res.json(products);
});

app.get("/products/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const product = products.find((p) => p.id === id);

  if (!product) {
    return res.status(404).json({ message: "Product not found" });
  }

  res.json(product);
});

app.listen(3000, () => {
  console.log("Product service running on port 3000");
});
