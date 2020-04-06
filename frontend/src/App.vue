<head>

</head>

<template>


  <div id="app">

    <div id="menu" style="margin-top:40px">
      <div >
        <!-- <vue-button type="default" v-on:click="goHome">Home</vue-button> -->
        <vue-button type="default" v-on:click="showModal({'name': 'upload-modal', 'title': 'Upload CSV File'})">Import CSV file</vue-button>
        <vue-button type="default" v-on:click="showModal({'name': 'filter-modal', 'title': 'Filter Table Data'})">Add/View Data Filters</vue-button>
        <!-- <vue-button type="default" v-on:click="showModal({'name': 'login-modal', 'fields': ['URL', 'Username', 'Password'], 'title': 'Login'})">Login</vue-button> -->
        <vue-button type="default" v-on:click="downloadReports">Export PDF</vue-button>
      </div>

    </div>

    <!-- <div id="drop_zone" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);"> -->
    <!-- <div>
      <ul>
        <li v-for="file in files">{{file.name}} - Error: {{file.error}}, Success: {{file.success}}</li>
      </ul>
      <file-upload
        ref="upload"
        v-model="files"
        post-action="/post.method"
        put-action="/put.method"
        @input-file="inputFile"
        @input-filter="inputFilter"
      >
      Upload file
      </file-upload>
      <button v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true" type="button">Start upload</button>
      <button v-show="$refs.upload && $refs.upload.active" @click.prevent="$refs.upload.active = false" type="button">Stop upload</button>
    </div> -->


    <div>
      <modal name="upload-modal" height="auto">
        <h2 align="center"> Upload Files(s) </h2>
        <div id="drop_zone" v-on:drop="dropHandler" v-on:dragover="dragOverHandler">
          <p align="center">Drag and drop files here</p>
          <template v-if="filenames.length > 0">
            <li v-for="file in filenames">
              {{ file }}
            </li>
          </template>
        </div>
        <div>
          <vue-button type="default" v-on:click="hideModal({'name': 'upload-modal'})">Cancel</vue-button>
          <vue-button type="default" v-on:click="getClasses() ; hideModal({'name': 'upload-modal'})">Upload CSV</vue-button>
          <!-- <vue-button type="default" v-on:click="submitInference() ; hideModal({'name': 'upload-modal'})">Upload</vue-button> -->
        </div>
      </modal>
    </div>

    <modal name="filter-modal" height="auto" >
      <h2 align="center"> Add Data Filter </h2>
      <!-- headers
      {{inference_headers}} -->
      <vue-form
        id="filter-form"
        :model="form">

        <vue-form-item >
          <!-- <v-select style="width:400px;margin-left:100px" id="filter_header" v-model="filter_header" placeholder="Column" :options=inference_headers></v-select> -->
          <template v-if="inference_headers && (inference_headers.length > 0)">
          <select v-model="filter_header">
            <option selected="selected">
              {{ inference_headers[0] }}
            </option>
            <option v-for="header in inference_headers.slice(1)">
              {{ header }}
            </option>
          </select>
          </template>
          <template v-else>
            <p style="color:red">No column titles found, please import CSV File</p>
          </template>

        </vue-form-item>

        <vue-form-item >
          <!-- <v-select style="width:400px;margin-left:100px" id="compare_type" v-model="compare_type" placeholder="Compare type" options="['less', 'greater', 'equal', 'contains']"></v-select> -->
          <select v-model="filter_compare_type">
            <option value="contains" selected="selected">Contains</option>
            <option value="less">Less</option>
            <option value="greater">Greater</option>
            <option value="equal">Equal</option>
          </select>
        </vue-form-item>
        <vue-form-item style="width:500px;" align=center>
          <vue-input
            placeholder="Value"
            v-model="filter_value">
          </vue-input>
        </vue-form-item>

        <vue-form-item style="margin-left:100px">
          <vue-button type="default" v-on:click="hideModal({'name': 'filter-modal'})">Cancel</vue-button>
          <vue-button type="success" v-on:click="addFilter() ; hideModal({'name': 'filter-modal'}) ">Add</vue-button>
        </vue-form-item>


        </vue-form>

        <h2 align="center"> Active Filters </h2>
        <template v-if="Object.keys(activeFilters).length > 0">
          <!-- {{activeFilters}} -->
          <div class="ui list">
            <template v-for="(value, key) in activeFilters">
              <div class="item">
                <div class="content"> </div>
                  <!-- <i class="window close outline icon" v-on:click="removeFilter(value)"></i>  -->
                  <div class="center floated description"> {{activeFilters[key].join(', ')}}
                  <div class="right floated content" v-on:click="removeFilter(value)">
                    <i class="window close outline icon"></i>
                    <div class="ui button">Remove</div>
                  </div>
                </div>

              </div>
            </template>

          </div>
        </template>

    </modal>

    <template v-if="(inference_rows.length > 0)">

      <!-- <data-table :data="inference_rows" :style="{overflow: 'auto'}">
      </data-table> -->
      <!-- <div class="ui container"> -->
      <div class="ui search" style="margin-top:30px;margin-bottom:30px;">
        <div class="ui icon input">
          <input v-model="search_query" v-on:keyup.enter="search" class="prompt" type="text" placeholder="Search Inferences">
          <i v-on:click="search" class="search icon"></i>
        </div>
        <div class="results"></div>
      </div>

      <template v-if="inference_rows_filtered.length > 0">
        Showing {{inference_rows_filtered.length}} of {{inference_rows.length}} rows
      </template>
      <template v-else>
        Showing all {{inference_rows.length}} rows
      </template>
      <table class="ui celled sortable table selectable compact scrolling" style="height:500px;overflow-x: scroll;">
        <thead class="sticky">
            <tr>
            <template v-for="header in inference_headers" >
              <th v-on:click=sortTable(header)>{{header}}</th>
            </template>
            </tr>
        </thead>
        <tbody>
          <template v-if="inference_rows_filtered.length > 0">
            <template v-for="row in inference_rows_filtered" >
              <tr>
                <template v-for="(value, label) in row" >
                  <!-- <td class="collapsing" :data-label=label>{{value}}</td> -->
                  <template v-if="label == 'Thumbnail'">
                    <td :data-label=label><img :src="'data:image/png;base64,' + value"/></img></td>
                  </template>
                  <template v-else-if="label == 'URL'">
                    <td :data-label=label></td>
                  </template>
                  <template v-else>
                    <td :data-label=label>{{value}}</td>
                  </template>

                </template>
              </tr>
            </template>
          </template>
          <template v-else>

            <template v-for="row in inference_rows" >
              <tr>
                <template v-for="(value, label) in row" >
                  <!-- <td class="collapsing" :data-label=label>{{value}}</td> -->
                  <template v-if="label == 'Thumbnail'">
                    <td :data-label=label><img :src="'data:image/png;base64,' + value"/></img></td>
                  </template>
                  <template v-else-if="label == 'URL'">
                    <td :data-label=label></td>
                  </template>

                  <template v-else>
                    <td :data-label=label>{{value}}</td>
                  </template>

                </template>
              </tr>
            </template>
          </template>
        </tbody>
      </table>


      <div class="ui card">
        <div class="content">
          <p class="header">Inference Stats</p>
        <div class="description">
          <p> {{inference_rows.length}} images uploaded </p>

          <template v-if="Object.keys(inference_results).length > 0">
              Images per Class
              <div class="extra content">

              <template v-for="(value, key) in inference_results">
                <p> {{key}} : {{value.length}} </p>
              </template>
              </div>
          </template>
        </div>
      </div>

      </div>

      <!-- <template for="">

      </template> -->

        <!-- <vuetable ref="vuetable"
          :api-mode="false"
          :data="inference_rows"
          :css="css.table"
          :fields="inference_headers"
          :multi-sort="true"
        >
        </vuetable> -->
      <!-- </div> -->

      <!-- <vuetable ref="vuetable"
        :api-mode="false"
        :data="inference_rows"
        :fields="['id', 'asset', 'vendor', 'status', 'lastmodifiedby', 'actions']"
      > -->
    </template>


    <template v-if="(selectedInference && (selectedInference.length > 0))">
      <h2> Detailed View </h2>
      <!-- <h3> {{inferences}} </h3> -->
      <!-- <h3> {{inferenceDetails}} </h3> -->
      <!-- <p>{{(inferences.filter( (i) => i._id == selectedInference))[0]}}</p> -->

      <!-- <source :src="url/uploads/inferences/7afb7810-bdfa-4968-aafc-06a8bd758f5b/training_video_out.mp4" type="video/mp4"> -->

      <md-card style="width:50%">
        <!-- <md-card-content> -->
        <!-- {{circleGraphData}} -->
        <Plotly id="detailedPieGraph" :data=circleGraphData :display-mode-bar="false"></Plotly>
        <!-- </md-card-content> -->
      </md-card>

      <md-card style="width:35%">
        <md-card-header>
          <md-card-header-text>
            <div class="md-title">Inference data</div>
          </md-card-header-text>
        </md-card-header>
        <!-- <md-card-content>
          <div class="md-subhead">Placeholder</div>
        </md-card-content> -->
        <md-card-content>
          <template v-if="inferenceDetails && (Object.keys(inferenceDetails).length > 0) && inferenceDetails[inference._id]">
            <div class="md-subhead">Detected Objects</div>
            <div>{{Object.keys(inferenceDetails[inference._id]).join(", ")}}</div>
          </template>
        </md-card-content>

      </md-card>
    </template>

    <!--  TODO, this is being hidden by datatables since it's fixed -->
    <!-- <div v-if="!isHidden" style="z-index:9000">
      <vue-form
        id="chaincode-form"
        :model="form"
        style="width: 75%; position: fixed; left: 50%; margin-left: -37.5%;">
        <h2 style="float:center"> Invoke Chaincode </h2>
        <vue-form-item label="Function">
          <vue-input
            placeholder="Function"
            v-model="form.function"
            style="width: 100%">
          </vue-input>
        </vue-form-item>

        <vue-form-item label="Arguments">
          <vue-input
            placeholder="Arguments"
            v-model="form.args"
            style="width: 100%">
          </vue-input>
        </vue-form-item>
        <vue-form-item>
          <vue-button type="default" v-on:click="isHidden = true">Cancel</vue-button>
          <vue-button type="success" v-on:click="invoke" >Submit</vue-button>
        </vue-form-item>
      </vue-form>
    </div> -->
    <!-- <vue-form-item> item 1 </vue-form-item>
      <vue-form-item> item 2 </vue-form-item> -->
    <!-- <vue-input placeholder="Please input"></vue-input>
      <vue-input placeholder="Please input"></vue-input> -->


    <!-- </v-app> -->
  </div>


</template>

<script>
  import 'vfc/dist/vfc.css'
  import './dist/json-tree.css'

  import {
    Input
  } from 'vfc'
  import {
    Form
  } from 'vfc'
  import {
    FormItem
  } from 'vfc'
  import {
    Button
  } from 'vfc'
  // import DemoLoginModal       from './components/modals/DemoLoginModal.vue'

  // import 'vue-js-modal'
  // import { Card } from 'v-card'
  // import { DataTable } from 'v-data-table'
  // import { Button } from 'vfc'



  export default {
    name: 'app',
    created() {
      var zip = new this.JSZip();
      var pdf = new this.jsPDF()
    },
    data() {
      return {
        isHidden: false,
        form: {
          function: '',
          args: ''
        },
        args: [],
        products: [],
        inferences: [],
        renderInferences: [],
        inference_data: {},
        fields: [],
        inference_rows: [],
        inference_headers: [],
        query: '',
        tableData: [],
        inference_rows_filtered: [],
        // token: (localStorage['token'] || ''),
        // user_fields: [],
        // user_type: '',
        // user_input: [],
        input: [],
        func: '',
        title: '',
        selectedInference: '',
        selectedModel: '',
        models: [],
        files: [],
        filenames: [],
        inference: {},
        inferenceDetails: {},
        lineGraphData: [],
        circleGraphData: [],
        activeFilters: {},
        sortAscending: true, //
        url: (localStorage['paiv_url'] || process.env.VUE_APP_URL),
        username: (localStorage['paiv_user'] || process.env.VUE_APP_USER),
        password: (localStorage['paiv_password'] || process.env.VUE_APP_PASSWORD),
        css: {
          table: {
            tableWrapper: '',
            tableHeaderClass: 'fixed',
            tableBodyClass: 'vuetable-semantic-no-top fixed',
            tableClass: 'ui blue selectable unstackable celled table',
            loadingClass: 'loading',
            ascendingIcon: 'blue chevron up icon',
            descendingIcon: 'blue chevron down icon',
            ascendingClass: 'sorted-asc',
            descendingClass: 'sorted-desc',
            sortableIcon: 'grey sort icon',
            handleIcon: 'grey sidebar icon'
          }
        },
        selected_compare: "",
        selected_header: "",
        value: "",
        filter_header: "",
        filter_value: "",
        filter_compare_type: "",
        search_query: "",
        inference_results: {},

        lineGraphLayout: {
          title: 'Objects Time Series',
          xaxis: {
            title: 'Seconds',
            showgrid: false,
            zeroline: false,
            tickmode: 'linear'
          },
          yaxis: {
            title: 'Objects',
            showline: false,
            dtick: 1
          }
        }

      }
    },
    components: {
      Form,
      FormItem,
      // DemoLoginModal,
      [Input.name]: Input,
      [Button.name]: Button
    },
    beforeMount() {

      // this.$data.selectedInference = "foobar"
      // this.getInferences()
    },
    mounted() {
      // this.getInferenceDetails();
      // this.getModels()
    },
    methods: {
      dragOverHandler(ev) {
        console.log('File(s) in drop zone');
        ev.preventDefault();
      },
      addFilter() {
        var filter_header = this.$data.filter_header
        var filter_compare_type = this.$data.filter_compare_type
        var filter_value = this.$data.filter_value
                // filter_header, filter_compare_type, filter_value
        // query column based on options
        // valid options are "less than", "greater than", "equal to", "contains"
        console.log("adding filter")
        console.log(filter_header, filter_compare_type, filter_value)
        var ts = Date.now()
        var filter = {}
        // filter[ts] = [filter_header, filter_compare_type, filter_value]
        this.$data.activeFilters[ts] = [filter_header, filter_compare_type, filter_value] //.push( filter )
        if (filter_compare_type == 'less') {
          var filtered_rows = this.$data.inference_rows.filter(row => row[filter_header] < filter_value)
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'greater') {
          var filtered_rows = this.$data.inference_rows.filter(row => row[filter_header] > filter_value)
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'equal') {
          var filtered_rows = this.$data.inference_rows.filter(row => row[filter_header] == filter_value)
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'contains') {
          var filtered_rows = this.$data.inference_rows.filter(row => row[filter_header].includes(filter_value))
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
          // console.log("filtered to " this.$data.inference_rows_filtered)
        }
      },
      removeFilter(f){
        console.log(f)
      },
      getClasses() {
        var delimiter = '__'
        this.$data.inference_results = {}
        this.$data.inference_rows.map( (row) => {
          console.log(row)
          var results = row['Metadata0']
          var scores = row['Metadata1']
          if (results.length > 0) {
            var top_result = results.split(delimiter)[0]
            var top_score = scores.split(delimiter)[0]
            console.log("top_result")
            console.log(top_result)
            if (Object.keys(this.$data.inference_results).includes(top_result) ) {
              this.$data.inference_results[top_result].push(top_score)
            } else {
              this.$data.inference_results[top_result] = [top_score]
            }
          }
          console.log("this.$data.inference_results")
          console.log(this.$data.inference_results)
        })

      },
      search() {
        var query = this.$data.search_query //this.$data.query
        console.log("performing search for: " + query)
        this.$data.inference_rows_filtered = this.$data.inference_rows.filter(row => JSON.stringify(row).includes(query))

        // TODO, allow multi search, split by query and
        // console.log("this.$data.inferenceDetails")
        // console.log(this.$data.inferenceDetails)
      },
      sortTable(column){
        // sort table by header
        console.log("sorting by " + column)
        var sortAscending = this.$data.sortAscending
        // TODO, add check to determine if all numbers
        // s.match(/^[0-9]+$/)
        if (sortAscending) {
          this.$data.inference_rows_filtered = this.$data.inference_rows.sort((a, b) => (a[column].toLowerCase() >= b[column].toLowerCase()) ? 1 : -1)
          this.$data.sortAscending = (! this.$data.sortAscending)
        } else {
          this.$data.inference_rows_filtered = this.$data.inference_rows.sort((a, b) => (a[column].toLowerCase() < b[column].toLowerCase()) ? 1 : -1)
          this.$data.sortAscending = (! this.$data.sortAscending)
        }

      },
      parseDate(d) {
        var dateObj = (new Date(Date.parse(d)))
        // var r = date.getMonth() + date.getDay() + date.getYear()
        var date = `${dateObj.getMonth()}/${dateObj.getDay()}/${dateObj.getFullYear()}`
        var time = dateObj.toLocaleString('en-US', {
          hour: 'numeric',
          minute: 'numeric',
          hour12: true
        })
        return `${date} ${time}`
      },
      forceFileDownload(response) {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'file.png') //or any other extension

        document.body.appendChild(link)
        link.click()
      },
      loadCSV() {
        // $data.rows =
      },
      downloadReports(){
        console.log("generating pdf")
        var pdf = new this.$jsPDF();
        var filename = "vis_insights_chart.pdf"

        if (this.$data.inference_rows_filtered.length > 0) {
          var rows = this.$data.inference_rows_filtered
          console.log("adding filtered rows to pdf")
        } else {
          var rows = this.$data.inference_rows
          console.log("adding all rows to pdf")
        }

        // doc.rect(40, 20, 10, 10); // filled square
        var headers = Object.keys(rows[0])

        // pdf.addPage('a4', 'p')
        var text_headers = ['DataSetName', 'Class', 'Score', 'URL', 'FormattedDate', 'Project' ]

        var inf_per_page = 5
        var num_pages = rows.length / inf_per_page
            // [...Array(num_pages - 1 ).keys()]

        // pdf.addPage('a4', 'p')
        // var p =
        // pdf.setPage(1)
        var createPages = new Promise( (resolve, reject) => {
          for (var i = 0 ; i < 12 ; i++ ) {
            pdf.addPage()
            if (i == 11) {
              resolve()
            }
          }
        })

        pdf.setPage(1)
        pdf.setFont("Arial");
        // pdf.setFontType("bold");
        pdf.setFontSize(30);
        pdf.text('Inference Results', 70, 20)
        pdf.setFontSize(9);
        var addInference = function(row, idx) {
            console.log(`------processing row ${idx}----------------------`)
            return new Promise( (resolve, reject) => {
              // console.log(`pdf ${JSON.stringify(pdf)}`)
              if ( (idx % inf_per_page == 0)) {
                console.log(`<---- turning to page ${idx / inf_per_page} ---->`)
                var currentPage = (idx / inf_per_page) + 1
                pdf.setPage((idx / inf_per_page) + 1)
              }

              // var currentPage = (idx / inf_per_page) + 1

              console.log(`adding inf on page ${currentPage}`)
              console.log(`row ${row}`)
              if (Object.keys(row).includes('Thumbnail') && (row['Thumbnail'].length > 0)) {
                var imageString = 'data:image/png;base64,' + row['Thumbnail'] // TODO, detect image typw
                // pdf.text(`image ${idx}`, 15, (40 * (idx + 1)))
                console.log(`image y ${(40 * (idx + 1 - currentPage))}`)
                pdf.addImage(imageString, 'PNG', 15, (50 * (( idx % inf_per_page ) + 1 )) , 45, 40)
              } else {
                console.log("no image, skipping this row")
                resolve()
              }

              text_headers.map( (h, h_idx) => {
                console.log(`adding inf header  ${h} on page ${currentPage}`)
                // 15, (50 * (( idx % inf_per_page ) + 1 ))
                // var text_headers = ['DataSetName', 'Class', 'Score', 'URL', 'FormattedDate', 'Project' ]
                pdf.text(`${h}: ${row[h]}`, 20 + 45, (50 * (( idx % inf_per_page ) + 1) + ((5 * (h_idx + 1))) ))

                // pdf.text(`${h}: ${row[h]}`, 15 + 45, 10 * (idx + h_idx + 4))
                if (h_idx == text_headers.length - 1 ) {
                    console.log("added all headers")
                    // pdf.line(20, 50 * (idx + 1), 60, 20)
                    // console.log(`pdf ${JSON.stringify(pdf)}`)
                    if (idx == (rows.length - 1) ) {
                      pdf.save(filename)
                      resolve()
                    } else {
                      resolve()
                    }
                    // console.log("waiting")
                    // setTimeout(function(){ resolve(); }, 1);

                    // resolve()

                }
              })
          })
        }

        var currentPage = 1
        createPages.then( () => {
          rows.reduce( (p, row, idx) => {
            return p.then(() => {
              // if ( (idx % inf_per_page == 0)) {
              //   console.log(`<---- turning to page ${ (idx / inf_per_page) + 1} ---->`)
              //   currentPage = (idx / inf_per_page) + 1
              //   pdf.setPage((idx / inf_per_page) + 1)
              // }
              return addInference(row, idx);
            });
          }, Promise.resolve());
          // rows.fill( addInference ).reduce( (p, f, i) => p.then(f), Promise.resolve() )

          // var promises = rows.map( (row, idx) => { addInference(row, idx)} )
          // console.log(promises[0])
          // console.log(promises[1])
          // promises.reduce( (p, f, i) => p.then(f), Promise.resolve() )
          /*
          https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises

          Sequential composition is possible using some clever JavaScript:

          [func1, func2, func3].reduce((p, f) => p.then(f), Promise.resolve())
          .then(result3 => { use result3 });
          Basically, we reduce an array of asynchronous functions down to a promise chain equivalent to: Promise.resolve().then(func1).then(func2).then(func3);
          */

          // Array.from({length:rows.length}, ()=> (addInference))

          // Array(rows.length).fill(addInference).reduce((p, f, i) => p.then(f), Promise.resolve())
          /*
          rows.reduce((promise, row, idx) => {
            console.log(`promise row ${row['Class']}`)
            console.log(`promise row ${idx}`)
            // resolve(item);
            return promise.then(() => {
              // return new Promise((resolve, reject)=> {
                return addInference(row, idx) //.then( () => {} )
              // })
            })
          }, Promise.resolve())
          */
        })


        // [func1, func2, func3].reduce((p, f) => p.then(f), Promise.resolve())


        /*
        var iterateRows(rows) {
          return rows.reduce((p, row) => {
            return promise.then( () => {
              return
            })
          })
        }
        */


        /*
        var currentPage = 1
        for (var i = 0 ; i < 5 ; i++ ) {
          pdf.addPage()
          if (i == 4) {
            rows.map( (row, idx) => {
              console.log(`row ${idx}`)

              // add image
              if (row['Thumbnail'] && row['Thumbnail'].length > 0) {
                var imageString = 'data:image/png;base64,' + row['Thumbnail'] // TODO, detect image type
                // console.log(`adding inf on page ${currentPage}`)
                pdf.addImage(imageString, 'PNG', 15, (40 * (idx + 1)) , 45, 40)
                pdf.text('DataSetName: ', 15, (50 * (idx + 1)))
                // pdf.text( row['DataSetName'], 150, 10 * (idx + 4))

                text_headers.map( (h, h_idx) => {
                  console.log(`adding inf header  ${h} on page ${currentPage}`)
                  pdf.text(`${h} - ${row[h]}`, 15, 10 * (idx + h_idx + 4))
                  if (h_idx == text_headers.length - 1 ) {
                      // pdf.line(20, 50 * (idx + 1), 60, 20)
                  }
                })
              }
              if ( (idx % inf_per_page == 0)) {
                console.log(`turning to page ${idx / inf_per_page}`)
                currentPage = idx / inf_per_page
                pdf.setPage(idx / inf_per_page)
              }

              if (idx == (rows.length - 1) ) {
                pdf.save(filename)
              }
            } )
          }
        }*/

        // Promise.all(Array(5).fill(createPagePromise)).then ( () => {
        //   console.log("created 5 pages")
        // Array(5).fill(pdf.addPage())
        // .reduce((p, f) => p.then(f), Promise.resolve()).then( () => {

          // })
        // } )
        // var processRow = new Promise( (resolve, reject) => {
        //   var imageString = 'data:image/png;base64,' + row['Thumbnail'] // TODO, detect image type
        //   console.log("imageString")
        //   console.log(imageString)
        //   pdf.addImage(imageString, 'PNG', 15, (40 * (idx + 1)) , 45, 40)
        //
        // } )







        // pdf.text(headers.join(','), 10, 0)

      },
      downloadImages() {
        var zip = new this.$JSZip();
        this.$data.renderInferences.map((inference, idx) => {
          if (inference['video_out']) { //(Object.keys(inference).includes("video_out") && inference['video_out'] != null) {
            var endpoint = inference.video_out
            console.log("requesting video at: " + endpoint)
          } else {
            var endpoint = inference.thumbnail_path
            console.log("requesting thumbnail at: " + endpoint)
          }
          var s = endpoint.split('/')
          var fileName = s[s.length - 1]
          var options = {
            headers: {
              'X-Proxy-URL': this.$data.url
            }
          }
          fetch('http://localhost:30000/proxyget' + endpoint, options).then((res) => {
            res.blob().then((content) => {
              if (idx == (this.$data.renderInferences.length - 1)) {
                console.log("adding " + fileName + " to zip")
                var z = zip.file(fileName, content)
                setTimeout(() => { // TODO, there definitely should be a better option than setTimeout, but jszip chaining isn't working
                  console.log("z.files")
                  console.log(z.files)
                  z.generateAsync({
                    type: "blob"
                  }).then((blob) => {
                    console.log("downloading zip")
                    const url = window.URL.createObjectURL(blob) //new Blob([blob]))
                    const link = document.createElement('a')
                    link.href = url
                    link.setAttribute('download', "images.zip") //or any other extension
                    document.body.appendChild(link)
                    link.click()
                  })
                }, 1000);
              } else {
                console.log("adding " + fileName + " to zip")
                zip.file(fileName, content)
              }
            })
          }).catch((err) => {
            console.log(err)
          })
        })
      },
      dropHandler(ev) {
        console.log('File(s) dropped');
        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
        this.$data.filenames = []
        if (ev.dataTransfer.items) {
          // Use DataTransferItemList interface to access the file(s)
          for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
              var file = ev.dataTransfer.items[i].getAsFile();
              // var meta = ev.dataTransfer.items[i].getMetadata();
              // console.log(meta)
              var s = file.text().then( (text) => {
                this.$data.inference_rows = []
                // this.$data.inference_headers = []
                var rows = text.split(/\r\n|\n/)
                var h = rows[0].split(',');
                this.$data.inference_headers = h
                // var headers = [h.map( (header) => { return {"text": header, "value": header } } )]
                var row_data = {}
                var h_obj = h.map( (h) => { row_data[h] = "" } )

                if (h_obj) {
                  rows.slice(1).map( (r, r_idx) => {
                      var row_elements = r.split(',')
                      var row_data_copy = Object.create(row_data)
                      row_elements.map( (c, idx) => {
                        // print(`adding column data ${c} ${idx}`)
                        row_data_copy[h[idx]] = c
                        // console.log( `${idx} / ${row.length - 1}` )
                        if (idx == (row_elements.length - 1)) {
                          console.log(`appending row ${r_idx}`)
                          console.log(JSON.stringify(row_data_copy))
                          this.$data.inference_rows.push(row_data_copy)
                        }
                      })
                  })
                }

                /*
                // row_data
                if (h_obj) {
                  rows.slice(1).map( (r, r_idx) => {
                      var row = r.split(',')
                      var row_data_copy = Object.create(row_data)
                      row.map( (c, idx) => {
                        // print(`adding column data ${c} ${idx}`)
                        row_data_copy[h[idx]] = c
                        // console.log( `${idx} / ${row.length - 1}` )
                        if (idx == (row.length - 1)) {
                          console.log(`appending row ${r_idx}`)
                          console.log(JSON.stringify(row_data_copy))
                          this.$data.inference_rows.push(row_data_copy)
                        }
                      })
                  })
                }
                */

              } ) //ev.dataTransfer.getData("text")

              console.log('... file[' + i + '].name = ' + file.name);
              console.log("printing text")

              this.$data.filenames.push(file.name)
              this.$data.files.push(file)
              // fetch(file).then( (response) => {
              //   response.text().then((text) => {
              //       console.log("file text")
              //       console.log(text)
              //     })
              //  })
             }
            }
          } else {
              // Use DataTransfer interface to access the file(s)
              for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);

              }
            }
      },
      login() {
        console.log("requesting token")
        console.log(this.$data.input)
        if (this.$data.input.length > 0) {
          localStorage.setItem('paiv_url', this.$data.input[0])
          localStorage.setItem('paiv_user', this.$data.input[1])
          localStorage.setItem('paiv_password', this.$data.input[2])

          this.$data.url = this.$data.input[0]
          this.$data.username = this.$data.input[1]
          this.$data.password = this.$data.input[2]
        }
        var options = {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            url: this.$data.input[0],
            username: this.$data.input[1],
            password: this.$data.input[2]
          })
        }
        fetch("http://localhost:30000/token", options).then((res) => {
          console.log("token api request made")
          this.$modal.hide("login-modal")
          res.text().then((token) => {
            console.log(`received new token ${token}`)
            this.$data.token = token
            localStorage.setItem('token', token)
            this.getModels()
            this.getInferences()
            this.getInferenceDetails()
            // pull data
          }).catch((err) => {
            console.log("err in token api promise")
            console.log(err)
          })
        })
      },
      inputFile: function(newFile, oldFile) {
        if (newFile && oldFile && !newFile.active && oldFile.active) {
          // Get response data
          console.log('response', newFile.response)
          if (newFile.xhr) {
            //  Get the response status code
            console.log('status', newFile.xhr.status)
          }
        }
      },
      inputFilter: function(newFile, oldFile, prevent) {
        if (newFile && !oldFile) {
          // Filter non-image file
          if (!/\.(jpeg|jpe|jpg|gif|png|webp)$/i.test(newFile.name)) {
            return prevent()
          }
        }

        // Create a blob field
        newFile.blob = ''
        let URL = window.URL || window.webkitURL
        if (URL && URL.createObjectURL) {
          newFile.blob = URL.createObjectURL(newFile.file)
        }
      },
      updateVideo(eventData) {
        // console.log("eventData")
        var x = eventData.points[0]['x']
        var vid = document.getElementById("videoContainer")
        vid.currentTime = x
        vid.play()
        console.log("skipping video to second:" + x)
        // this.$refs["videoContainer"]
        // console.log(this.$refs["detailedGraph"])
        // console.log(this.$refs["detailedGraph"].$el._fullData[0].selected.markers.toString())
        // console.log(this.$refs["detailedGraph"].$el._fullData[0])
      },
      submitInference() {
        // post to powerai when user clicks "upload"
        var e = document.getElementById("selectedModel");
        var selectedModel = e.options[e.selectedIndex].value
        this.$data.selectedModel = selectedModel //'ee5f1177-7ff1-4cd5-86d2-60faca266c71'
        this.$data.files.map((file, f_idx) => {
          var formData = new FormData()
          formData.append('blob', file)
          formData.append("genCaption", "true")
          var options = {
            method: "POST",
            body: formData,
            headers: {
              // "X-Auth-Token": this.$data.token,
              "X-Proxy-URL": this.$data.url
            //   // "Content-Type": "multipart/form-data"
            }
          }
          console.log("formData")
          console.log(formData)
          console.log("adding file: " + file.name)
          // console.log('this.$data.url + "/dlapis/" + this.$data.selectedModel')
          // console.log(this.$data.url + "/dlapis/" + this.$data.selectedModel)
          // fetch(this.$data.url + "/dlapis/" + this.$data.selectedModel, options).then((res) => {
          console.log("posting to: " + "http://localhost:30000/proxypost" + "/api/dlapis/" + selectedModel)
          fetch("http://localhost:30000/proxypost" + "/api/dlapis/" + this.$data.selectedModel, options).then((res) => {
            console.log("api call complete")
            // this.$modal.hide('invoke-modal');
            // console.log(res.text())
            console.log(res)
            res.json().then((result) => {
              console.log("json")
              console.log(result)
              // this.$data.inferences.append(result)
              // TODO, this only applies in case of a still image
              var labels = Array.from(new Set(result.classified.map((c) => c.label)))
              var endpoint = result.imageUrl.split('/uploads')[1]
              // result.classified.filter((c) =>  )
              this.$data.inferenceDetails[result.imageMd5] = {}
              labels.map((l) => {
                var r = result.classified.filter(c => c.label == l)
                var count = r.length //Array.from((new Set(r))).length
                console.log("count for " + l)
                this.$data.inferenceDetails[result.imageMd5][l] = count
              })

              var inference = {
                _id: result.imageMd5,
                created_date: (new Date().toJSON()),
                thumbnail_path: '/uploads' + endpoint,
                status: result['result'],
                model: result['webAPIId'],
                percent_complete: 100
              }
              console.log("labels")
              console.log(labels)
              // this.$data.inferenceDetails[result.imageMd5] =  //result.classified
              console.log("appending inference ")
              console.log(inference)
              this.$data.inferences.push(inference)
            }).catch((err) => {
              console.log("error parsing json")
            })
          }).catch((err) => {
            console.log(err)
          })
          if (f_idx == (this.$data.files.length - 1)) {
            this.$data.files = []
          }
        })
      },
      postInference() {
        var options = {
          method: "POST",
          body: file
          // headers: {
          //   'Accept': 'application/json',
          //   'Content-Type': 'application/json'
          // }
        }
        const input = document.getElementById('fileinput');
        const file = input.files[0]
        fetch("http://localhost:30000/inferences", options).then((response) => {
          response.json().then((json) => {
            // TODO filter is only here to ignore shared inferences
            this.$data.inferences = inf; // json
            this.$data.renderInferences = inf //.filter(i => i.model_id == '3ac091c7-66ef-450a-8b7d-fa9e0cc748e6 	') // only need to do this initially
            console.log("inferences received")
            // localStorage.setItem('inferences', inferences)
          })
        })
      },
      getInferences() {
        return new Promise((resolve, reject) => {
          var options = {
            method: "GET",
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              "X-Proxy-URL": this.$data.url,
              "X-Auth-Token": this.$data.token
            }
          }
          fetch("http://localhost:30000/inferences", options).then((response) => {
            response.json().then((json) => {
              // TODO filter is only here to ignore shared inferences
              var inf = json //.filter(i => i.model_id != '29dad520-4908-42fc-b118-9971b957bf8c')
              this.$data.inferences = inf; // json
              this.$data.renderInferences = inf //.filter(i => i.model_id == '3ac091c7-66ef-450a-8b7d-fa9e0cc748e6 	') // only need to do this initially
              resolve(inf)
              console.log("inferences received")
              // localStorage.setItem('inferences', inferences)
            })
          })
        })
      },
      getInferenceDetails() {
        var options = {
          method: "GET",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }
        setTimeout(() => {
          fetch("http://localhost:30000/inferencedetailed", options).then((response) => {
            console.log(response)
            response.json().then((json) => {
              console.log("inference details received")
              console.log(JSON.stringify(json))
              this.$data.inferenceDetails = json
            }).catch((err) => {
              console.log("failure receiving detailed data")
              console.log(err)
            })
          })
        }, 2000)

      },
      setInference(inferenceId) {
        console.log("setting inference")
        // console.log(event.explicitOriginalTarget.offsetParent.offsetParent)
        // var inference = event.explicitOriginalTarget.offsetParent.offsetParent.attributes['inference'].nodeValue
        console.log(inferenceId)
        this.$data.selectedInference = inferenceId
        // self.getInferenceDetails()
        // self.formatLine(inferenceId)
        // selectedInference
      },
      formatLine(inferenceId) {
        if (this.$data.inferenceDetails) {
        console.log("generating line graph for " + inferenceId)
        console.log(this.$data.inferenceDetails[inferenceId])
        var detections = this.$data.inferenceDetails[inferenceId]
        var objects = Object.keys(detections)
        var d = []
        objects.map((o) => {
          var x = Array.from(Array(detections[o].length + 1).keys())
          // d['data'].push({
          d.push({
            x: [0].concat(x),
            y: [0].concat(detections[o]),
            mode: 'lines',
            type: 'scatter',
            name: o
            // mode:"lines+markers"
          })
          console.log(d)
        })

        this.$data.lineGraphData = d
        console.log("this.$data.lineGraphData")
        console.log(this.$data.lineGraphData)
        // detections.map( (detection) )
        }
        // this.$data.lineGraph =
        // this.$data.circleGraph =
      },
      formatCircle(inferenceId) {
        console.log(this.$data.inferenceDetails)
        console.log("generating line graph for " + inferenceId)
        var detections = this.$data.inferenceDetails[inferenceId]
        var objects = Object.keys(detections)
        var d = {
          values: [],
          labels: [],
          type: "pie",
          textinfo: "label+percent",
          textposition: "outside",
          automargin: true
        }
        objects.map((o) => {
          d['values'].push(detections[o].reduce((a, b) => a + b, 0))
          d['labels'].push(o)
          console.log(d)
        })

        this.$data.circleGraphData = [d]
        console.log("this.$data.circleGraphData")
        console.log(this.$data.circleGraphData)
      },
      showInvokeModal(config) {
        console.log("opening modal")
        // console.log(fields)
        this.$data.input = []
        console.log(config.function)
        console.log(config.fields)
        this.$data.func = config.function
        this.$data.fields = config.fields
        this.$data.title = config.title
        this.$data.user_fields = []
        this.$data.user_type = ''
        this.$modal.show('invoke-modal', {
          "fields": config.fields
        });
      },
      showModal(config) {
        console.log("opening modal")
        this.$data.fields = config.fields
        this.$data.title = config.title
        // console.log(fields)
        // this.$data.input = []
        this.$modal.show(config.name, {
          "fields": config.fields
        });
      },
      hideModal(config) {
        this.$modal.hide(config.name);
        console.log("hiding modal: " + config.name)
        // this.$data.user_fields = []
        // this.$data.user_type = ''
      },
      getFormValues() {
        console.log("getting form vals")
        console.log(this.$data.input)
        // this.output = this.$refs.my_input.value
        // console.log(this.$refs.my_input.value)
      },
      goHome() {
        this.$data.selectedInference = null
        this.$data.renderInferences = this.$data.inferences
      },
    },
    filters: {
      pretty: function(value) {
        return JSON.stringify(value, null, 2);
      }
    }


  }
</script>

<!-- TODO, finish modal -->
<!-- <script type="text/x-template" id="modal-template">
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            <slot name="header">
              default header
            </slot>
          </div>

          <div class="modal-body">
            <slot name="body">
              default body
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              default footer
              <button class="modal-default-button" @click="$emit('close')">
                OK
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</script> -->


<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  #drop_zone {
    border: 2px dashed #eaecee;
    width: 400px;
    height: 300px;
    margin: auto;
  }


  select {
    margin: 50px;
    padding: 5px 35px 5px 5px;
    font-size: 16px;
    border: 1px solid #666666;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
  }

</style>

<!-- <style lang="scss" scoped>
  .md-card {
    width: 320px;
    margin: 40px;
    display: inline-block;
    vertical-align: top;
  }
</style> -->
