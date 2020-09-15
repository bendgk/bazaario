<template>
  <v-app id="app" class="grey--color">
    <v-row>
      <v-col class="col-3">
        <v-card>
          <v-text-field label="Search" single-line outlined v-model="searchTerm" @input="searchHandler">
          </v-text-field>
          <v-virtual-scroll
            :items="visibleProducts"
            height="600"
            item-height="42"
          >
            <template v-slot="{ item }">
              <v-list-item :key="item">
                <v-list-item-content>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-list-item-title v-on="on" v-bind="attrs" v-on:click="loadProduct(item)"> {{ item }} </v-list-item-title>
                    </template>
                    <span>
                      {{item}} //TODO: SHOW MORE INFO
                    </span>
                  </v-tooltip>
                  <v-divider></v-divider>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-virtual-scroll>
        </v-card>
      </v-col>
      <v-col class="col-9">
        <h1>Bazaario</h1>
        <div id="graph"></div>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
import $ from 'jquery'
import axios from 'axios'

//Lightweight-Charts
import { createChart } from 'lightweight-charts';

export default {
  name: "App",

  data: () => ({
    products: [],
    visibleProducts: [],
    chart: null,
    lineSeries: null,
    price: 0,
    searchTerm: "",
  }),

  components: {

  },

  mounted: function() {
    this.chart = createChart(document.getElementById("graph"), { width: document.width, height: 650});
    this.lineSeries = this.chart.addLineSeries();

    this.getProducts()
  },

  created() {
    window.addEventListener("resize", this.resizeEventHandler);
  },
  destroyed() {
    window.removeEventListener("resize", this.resizeEventHandler);
  },

  methods: {
    resizeEventHandler(e) {
      console.log(this.products)
      this.chart.resize($("#graph").width(), 650)
    },

    getProducts() {
      axios.get('http://157.245.135.17:3000/getProducts').then(data => {
        this.products = data["data"]
        this.visibleProducts = data["data"]
      })
    },

    loadProduct(product) {
      axios.get('http://157.245.135.17:3000/timeSeries/' + product).then(data => {
        this.price = data["data"][0]["value"]

        this.chart.removeSeries(this.lineSeries)
        this.lineSeries = this.chart.addLineSeries({
          autoscaleInfoProvider: () => ({
            priceRange: {
              minValue: this.price - (this.price * .10),
              maxValue: this.price + (this.price * .10),
            },

            margins: {
              above: 10,
              below: 10,
            }
          })
        });
        this.lineSeries.setData(data["data"])
      })
    },

    searchHandler() {
      this.visibleProducts = []
      this.products.forEach(item => {
        if (item.toLowerCase().indexOf(this.searchTerm.toLowerCase()) != -1) {
          this.visibleProducts.push(item)
        }
      })
    }
  }
}
</script>

<style scoped>
</style>
