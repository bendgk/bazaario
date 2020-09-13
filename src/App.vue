<template>
  <v-app id="app" class="grey--color">
    <v-row>
      <v-col class="col-3">
        <v-card>
          <v-text-field label="Search" single-line outlined>
          </v-text-field>
          <v-virtual-scroll
            :items="products"
            height="600"
            item-height="42"
          >
            <template v-slot="{ item }">
              <v-list-item :key="item">
                <v-list-item-content>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-list-item-title v-on="on" v-bind="attrs"> {{ item }} </v-list-item-title>
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
    chart: null,
    lineSeries: null,
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
      axios.get('http://127.0.0.1:3000/getProducts').then(data => {
        this.products = data["data"]
      })

      axios.get('http://127.0.0.1:3000/timeSeries/GRAVEL').then(data => {
        console.log(data["data"])
        this.lineSeries.setData(data["data"])
      })
    }
  }
}
</script>

<style scoped>
</style>
