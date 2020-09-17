//express
const express = require('express')
const app = express()
const port = 3000

//headers
app.use((req, res, next) => {
  const allowedOrigins = ['http://127.0.0.1:8080', 'http://localhost:8080', 'http://127.0.0.1:9000', 'http://157.245.135.17:8080', 'http://bazaario.xyz:8080', 'http://www.bazaario.xyz:8080'];
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
       res.setHeader('Access-Control-Allow-Origin', origin);
  }
  //res.header('Access-Control-Allow-Origin', 'http://127.0.0.1:8020');
  res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.header('Access-Control-Allow-Credentials', true);
  return next();
});

//MongoDB
const MongoClient = require('mongodb').MongoClient
var db
var cols = []
MongoClient.connect('mongodb://bendgk:!MyMongoDBPassword@127.0.0.1:27017/tickers', (err, client) => {
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
