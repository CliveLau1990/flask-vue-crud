<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>TestSuite: {{ project }}</h1>
        <hr>
        <alert :message=message v-if="showMessage"></alert>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Index</th>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">Min</th>
              <th scope="col">Typical</th>
              <th scope="col">Max</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(suite, index) in suites" :key="index">
              <td>{{ suite.index }}</td>
              <td>{{ suite.title }}</td>
              <td>{{ suite.description }}</td>
              <td>{{ suite.min }}</td>
              <td>{{ suite.typical }}</td>
              <td>{{ suite.max }}</td>
              <td>
                <span v-if="suite.status === 'inprocess'">
                  <!-- <b-spinner variant="success"
                             type="grow"
                             label="Spinning">
                  </b-spinner> -->
                  <!-- <i class="fa fa-check-square" style="font-size:24px;color:green"></i> -->
                  <i class="fa fa-times-circle" style="font-size:24px;color:red"></i>
                </span>
                <span v-else-if="suite.status === 'pass'">Pass</span>
                <span v-else-if="suite.status === 'fail'">Fail</span>
                <span v-else>Init</span>
              </td>
            </tr>
          </tbody>
        </table>
        <button type="button"
                class="btn btn-warning btn-sm"
                @click="onStart()">
            Start
        </button>
        <button type="button"
                class="btn btn-danger btn-sm"
                @click="onStop()">
            Stop
        </button>
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
          this.suites = res.data.suite;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    startSuites() {
      const path = 'http://localhost:5000/testsuite';
      axios.post(path)
        .then(() => {
          this.getSuites();
          this.message = 'Testing';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSuites();
        });
    },
    onStart() {
      clearInterval(this.timer);
      this.timer = setInterval(() => {
        this.getSuites();
      }, 3000);
      this.startSuites();
    },
    onStop() {
      clearInterval(this.timer);
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
