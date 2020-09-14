//express
const express = require('express')
const app = express()
const port = 3000

//headers
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', 'http://157.245.135.17:8080');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type,Authorization,Access-Control-Allow-Origin');
  res.setHeader('Access-Control-Allow-Credentials', true);
  next();
});

//MongoDB
const MongoClient = require('mongodb').MongoClient
var db
var cols = []
MongoClient.connect('mongodb://127.0.0.1:27017', (err, client) => {
  if (err) return console.error(err)
  console.log('Connected to Database')

  db = client.db('tickers')
  db.listCollections().toArray().then(data => {
    data.forEach(item => cols.push(item["name"]))
  })
})

//routes
app.get('/getProducts', (req, res) => {
  res.json(cols)
})

app.get('/timeSeries/:product', function (req, res) {
  const product = req.params['product']
  if (!cols.includes(product)) res.send(false)
  db.collection(product).aggregate(
    [
      {$addFields: {"value": "$ask_price"}},
      {
        $project: {_id: 0, bid_price: 0, sell_orders: 0, buy_orders: 0, sell_volume: 0, buy_volume: 0, ask_price: 0}
      }
    ]).sort({time: -1}).limit(500).toArray().then(data => {
    res.send(data)
  }).catch(err => {
    console.log(err)
  })
}) 

app.listen(port, () => {
  console.log(`Bazaario backend at http://localhost:${port}`)
})
