<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test Suite: {{ project }}</h1>
        <hr>
          <alert :message=message v-if="showMessage"></alert>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Index</th>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">Min</th>
              <th scope="col">Typical</th>
              <th scope="col">Max</th>
              <th scope="col">Value</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(suite, index) in suites" :key="index">
              <td align="center">{{ suite.index }}</td>
              <td align="left">{{ suite.title }}</td>
              <td align="left">{{ suite.description }}</td>
              <td align="center">{{ suite.min }}</td>
              <td align="center">{{ suite.typical }}</td>
              <td align="center">{{ suite.max }}</td>
              <td align="center">{{ suite.value }}</td>
              <td align="center">
                <span v-if="suite.status === 'inprocess'">
                  <b-spinner variant="success"
                             type="grow"
                             label="Spinning">
                  </b-spinner>
                </span>
                <span v-else-if="suite.status === 'pass'">
                  <i class="fa fa-check-circle-o" style="font-size:24px;color:green"></i>
                </span>
                <span v-else-if="suite.status === 'fail'">
                  <i class="fa fa-times-circle" style="font-size:24px;color:red"></i>
                </span>
                <span v-else></span>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="btn-group pull-right"
             role="group">
          <button type="button"
                  class="btn btn-warning btn-lg"
                  @click="onStart()">
              Start
          </button>
          <button type="button"
                  class="btn btn-danger btn-lg"
                  style="margin-left:10px"
                  @click="onStop()">
              Stop
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      message: '',
      showMessage: false,
      project: '',
      caseidx: 0,
      suites: [],
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getSuites() {
      const path = 'http://localhost:5000/testsuite';
      axios.get(path)
        .then((res) => {
          this.project = res.data.project;
          this.caseidx = res.data.caseidx;
          window.console.log('<getSuites> called');
          window.console.log(this.caseidx);
          this.suites = res.data.suite;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    startSuites() {
      const path = 'http://localhost:5000/testcase/start';
      axios.post(path)
        .then(() => {
          this.getSuites();
          window.console.log('Start testing');
          this.message = 'Start testing';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSuites();
        });
    },
    stopSuites() {
      const path = 'http://localhost:5000/testcase/stop';
      axios.post(path)
        .then(() => {
          // this.getSuites();
          window.console.log('Stop testing');
          this.message = 'Stop testing';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSuites();
        });
    },
    generateReport() {
      const path = 'http://localhost:5000/testcase/report';
      axios.post(path)
        .then(() => {
          // this.getSuites();
          window.console.log('Generating Report!');
          this.message = 'Generating Report!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSuites();
        });

      this.onStart();
    },
    onStart() {
      window.console.log('onStart');
      clearInterval(this.timer);
      this.getSuites();
      this.timer = setInterval(() => {
        this.getSuites();
        // TODO: 判断是否执行有误
        if (this.suites[this.caseidx].status === 'fail') {
          this.onStop();
        } else if ((this.caseidx + 1) === this.suites.length) {
          if (this.suites[this.caseidx].status === 'pass'
              || this.suites[this.caseidx].status === 'fail') {
            window.console.log('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
            window.console.log(this.caseidx);
            window.console.log(this.suites[this.caseidx].status);
            this.onStop();
            this.generateReport();
          }
        }
      }, 500);
      this.startSuites();
    },
    onStop() {
      clearInterval(this.timer);
      this.stopSuites();
    },
  },
  created() {
    this.getSuites();
  },
  destroyed() {
    clearInterval(this.timer);
  },
};
</script>
