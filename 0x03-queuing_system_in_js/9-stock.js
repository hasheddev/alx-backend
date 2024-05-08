import { createClient, print } from "redis";
import express from 'express';
import { promisify } from 'util';

const client = createClient();

const app = express();

const listProducts = [
  { Id: 1, name: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { Id: 2, name: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { Id: 3, name: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { Id: 4, name: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
]

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const getAsync = promisify(client.get).bind(client);

function getItemById(id) {
  return listProducts.find((product => product.Id === id));
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(itemId);
  return stock;
}

app.get('/list_products', (req, res) => {
  return res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const stock = await getCurrentReservedStockById(itemId);
  const item = getItemById(parseInt(itemId));
  const currentQuantity = (stock === null) ? item.initialAvailableQuantity : parseInt(stock);
  if (item) {
    const currentItem = {
      ...item,
      currentQuantity
    }
    return res.json(currentItem);
  }
  return res.json({ status:"Product not found" });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) {
   return res.json({ status:"Product not found" });
  }
  const stock = await getCurrentReservedStockById(itemId);
  if (stock !== null) {
    const currentStock = parseInt(stock);
    if (currentStock > 0) {
      reserveStockById(itemId, currentStock - 1);
      return res.json({ "status":"Reservation confirmed", itemId });
    } else {
      return res.json({ "status": "Not enough stock available", itemId });
    }
  } else {
    reserveStockById(itemId, item.initialAvailableQuantity - 1);
    return res.json({ "status":"Reservation confirmed", itemId });
  }
});

const port = 1245;

app.listen(port);
