/* eslint-disable */
<template>


  <div id="app">
    <div id="menu" style="margin-top:40px">
      <div >
        <!-- <vue-button type="default" v-on:click="showModal({'name': 'upload-modal', 'title': 'Upload CSV File'})">Import CSV file</vue-button>
        <vue-button type="default" v-on:click="showModal({'name': 'filter-modal', 'title': 'Filter Table Data'})">Add/View Data Filters</vue-button>
        <vue-button type="default" v-on:click="downloadReports">Export PDF</vue-button> -->

        <CvButton style="margin: 0px 10px; text-align: center" type="default" v-on:click="showModal({'name': 'upload-modal', 'title': 'Upload CSV File'})">Import CSV file</CvButton>
        <CvButton style="margin: 0px 10px; text-align: center" type="default" v-on:click="showModal({'name': 'filter-modal', 'title': 'Filter Table Data'})">Add/View Data Filters</CvButton>
        <CvButton style="margin: 0px 10px; text-align: center" type="default" v-on:click="printElem">Export PDF</CvButton>
      </div>
    </div>

    <!-- <div v-if="inference_rows && (inference_rows.length > 0)">
      Rendered Table Component
      <template >
        <inf-table inference_headers="inference_headers" inference_rows="inference_rows">
        </inf-table>
      </template>
      End Rendered Table Component
    </div> -->
    <div>


      <modal name="upload-modal" height="auto">

        <h2 align="center"> Upload Files(s) </h2>
        <div id="drop_zone" v-on:drop="dropHandler" v-on:dragover="dragOverHandler">
          <div style="margin: 0 auto;width: 60%">
            <cv-file-uploader
              :label="label"
              :helperText="helperText"
              :drop-target-label="dropTargetLabel"
              :accept="accept"
              :clear-on-reselect="clearOnReselect"
              :initial-state-uploading="initialStateUploading"
              :multiple="multiple"
              :removable="removable"
              :remove-aria-label="removeAriaLabel"
              ref="fileUploader">
            </cv-file-uploader>
          </div>

          <!-- <template v-if="filenames.length > 0">
            <li v-for="file in filenames">
              {{ file }}
            </li> -->
          <!-- </template> -->
        </div>
        <div style="display: table; margin: 0 auto;">
          <div >

            <!-- <vue-button type="default" v-on:click="hideModal({'name': 'upload-modal'})">Cancel</vue-button>
            <vue-button type="default" v-on:click="hideModal({'name': 'upload-modal'}) ; getClasses() ; formatCircle() ">Upload CSV</vue-button> -->
            <CvButton style="margin: 0px 10px; text-align: center" type="default" v-on:click="showModal({'name': 'filter-modal', 'title': 'Filter Table Data'})">Upload CSV</CvButton>
            <CvButton style="margin: 0px 10px; text-align: center" type="default" v-on:click="printElem">Cancel</CvButton>

            <!-- <vue-button type="default" v-on:click="submitInference() ; hideModal({'name': 'upload-modal'})">Upload</vue-button> -->
          </div>

        </div>
      </modal>
    </div>

    <!-- TODO draw rect -->
    <!-- <vue-button type="default" v-on:click="showModal({'name': 'view-image'})">Image</vue-button> -->
    <div style="margin: 0; position: absolute; top: 50%; left: 50%;" >
      <modal name="view-image" height="auto" >
        <h2 align="center"> Image </h2>
        <!-- {{inference}} -->
        <!-- <h2 align="center"> {{inference}} </h2> -->
        <div>
          <canvas id="image_canvas" v-overlay-image="inference"></canvas>
          <!-- <img :src=src><img/> -->
        </div>
        <div>
          <vue-button type="default" v-on:click="hideModal({'name': 'view-image'})">Cancel</vue-button>
        </div>
      </modal>
    </div>

    <modal name="filter-modal" height="auto" >
      <h2 align="center"> Add Data Filter </h2>
      <!-- headers
      {{inference_headers}} -->
      <template v-if="inference_headers && (inference_headers.length > 0)">
        <vue-form
          id="filter-form"
          :model="form">

          <vue-form-item >
            <!-- <v-select style="width:400px;margin-left:100px" id="filter_header" v-model="filter_header" placeholder="Column" :options=inference_headers></v-select> -->

            <select v-model="filter_header">
              <option value="" disabled selected>Select Column</option>
              <option selected="selected">
                {{ inference_headers[0] }}
              </option>
              <option v-for="header in inference_headers.slice(1)">
                {{ header }}
              </option>
            </select>

          </vue-form-item>

          <vue-form-item >
            <!-- <v-select style="width:400px;margin-left:100px" id="compare_type" v-model="compare_type" placeholder="Compare type" options="['less', 'greater', 'equal', 'contains']"></v-select> -->
            <select v-model="filter_compare_type">
              <option value="" disabled selected>Select Comparison Type</option>
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

        </template>
        <template v-else>
          <p style="color:red">No column titles found, please import CSV File</p>
        </template>

        <h2 align="center"> Active Filters </h2>
        <template v-if="Object.keys(activeFilters).length > 0">
          <!-- {{activeFilters}} -->
          <div class="ui list">
            <template v-for="(value, key) in activeFilters">
              <div class="item">
                <div class="content"> </div>
                  <!-- <i class="window close outline icon" v-on:click="removeFilter(value)"></i>  -->
                  <div class="center floated description"> {{activeFilters[key].join(', ')}}
                    <!-- <div class="right floated content" v-on:click="removeFilter(value)">
                      <i class="window close outline icon"></i>
                      <div class="ui button">Remove</div>
                    </div> -->
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
          <input v-model="search_query" @input="search" v-on:keyup.enter="search" class="prompt" type="text" placeholder="Search Inferences">
          <i v-on:click="search" class="search icon"></i>
        </div>
        <div class="results"></div>

      </div>
      <div>

        <template v-if="inference_rows_filtered.length > 0">
          Showing {{inference_rows_filtered.length}} of {{inference_rows.length}} rows
        </template>
        <template v-else>
          Showing all {{inference_rows.length}} rows
        </template>

      </div>
      <!--
      TODO, figure out carbon modal
      <button @click="show">Show</button>
      <cv-modal
        :close-aria-label="closeAriaLabel"
        :size="size"
        :visible="visible"
        @modal-shown="actionShown"
        @modal-hidden="actionHidden"
        @modal-hide-request="actionHideRequest"
        :auto-hide-off="autoHideOff">
        <template v-if="use_label" slot="label">Label of modal</template>
        <template v-if="use_title" slot="title">Title of modal</template>
        <template v-if="use_content" slot="content"><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, seed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></template>
      </cv-modal> -->

      <!-- CARBON DATATABLE -->
      <!-- <cv-data-table
        :columns="inference_headers" -->

    <div id="table_container">
     <div style="margin: auto;width: 80%">
      <cv-data-table
        :columns="inference_headers"
        :pagination="basicPagination"
        ref="table">
        <template v-if="inference_rows && (inference_rows.length > 0)" v-for="row in inference_rows" slot="data">
          <!-- <cv-data-table-row v-for="(row, rowIndex) in [`ibm`, `beta`, `local`, `custom`, `private`]" :key="`${rowIndex}`" :value="`${rowIndex}`"> -->
          <cv-data-table-row>

            <template v-if="Object.keys(row).includes('Thumbnail')">
              <cv-data-table-cell ><img v-on:click="showModal({'name': 'view-image', 'inference': row})" :src="'data:image/png;base64,' + row['Thumbnail']"></img></cv-data-table-cell>
            </template>

             <template v-if="Object.keys(row).includes('ImageURL')">
               <cv-data-table-cell>
                 <img v-on:click="showModal({'name': 'view-image', 'inference': row})" style="width:300px;height:175px" :src="row['ImageURL']"/></img>
               </cv-data-table-cell>
             </template>

             <template v-if="Object.keys(row).includes('InferenceType')">
               <cv-data-table-cell>
                 <p>{{row['InferenceType']}}</p>
               </cv-data-table-cell>
             </template>


             <!-- <template v-if="Object.keys(row).includes('DataSetName')">
               <cv-data-table-cell >{{row['DataSetName']}}</cv-data-table-cell>
             </template> -->


             <!-- <template v-if="Object.keys(row).includes('Location')">
               <cv-data-table-cell >{{row['Location']}}</cv-data-table-cell>
             </template> -->

             <template v-if="Object.keys(row).includes('Heatmap/Boxes') && (row['Heatmap/Boxes'].length > 500 )">
               <cv-data-table-cell ><img :src="'data:image/png;base64,' + row['Heatmap/Boxes']"></img></cv-data-table-cell>
             </template>
             <template v-else-if="Object.keys(row).includes('Heatmap/Boxes') && (row['Heatmap/Boxes'].includes('|'))">
               <cv-data-table-cell >
                 <li v-for="box in row['Heatmap/Boxes'].split('|')">
                     {{box}}
                 </li>
               </cv-data-table-cell>
             </template>
             <template v-else>
               {{row['Heatmap/Boxes']}}
             </template>


             <cv-data-table-cell>
               <template v-if="row['Class'].includes('|')">
                  <li v-for="cls in row['Class'].split('|')">
                      {{cls}}
                  </li>
               </template>
               <template v-else>
                   {{row['Class']}}
               </template>
             </cv-data-table-cell>

             <cv-data-table-cell>
               <template v-if="row['Score'].includes('|')">
                  <li v-for="score in row['Score'].split('|')">
                      {{score}}
                  </li>
               </template>
               <template v-else>
                   {{row['Score']}}
               </template>
             </cv-data-table-cell>

             <template v-if="Object.keys(row).includes('Time')">
               <cv-data-table-cell>
                 <p>{{row['Time']}}</p>
               </cv-data-table-cell>
             </template>

             <template v-if="Object.keys(row).includes('FormattedDate')">
               <cv-data-table-cell >{{row['FormattedDate']}}</cv-data-table-cell>
             </template>

             <!-- <cv-data-table-cell>
               <p>{{row['']}}</p>
             </cv-data-table-cell> -->

          </cv-data-table-row>
        </template>
      </cv-data-table>
     </div>
    </div>




      <div class="ui card" style="margin-left: auto;margin-right: auto; width:40%">
        <h2 class="header">Inference Stats</h2>
        <div class="content">
          <!-- <p class="header">Inference Stats</p> -->

        <div class="description">
          <p> {{inference_rows.length}} images uploaded </p>
        </div>
      </div>
        <div class="content">
          <h3 class="header">Images per Class</h3>
          <template v-if="Object.keys(inference_results).length > 0">
              <!-- <div class="content"> -->

                <!-- <template v-for="(value, key) in inference_results">
                  <p> {{key}} : {{value.length}} </p>
                </template> -->

                <Plotly id="detailedPieGraph" :data=circleGraphData :display-mode-bar="false"></Plotly>

              <!-- </div> -->
          </template>
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
        <Plotly id="detailedPieGraph" :data=circleGraphData :display-mode-bar="true"></Plotly>
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

    directives: {
      overlayImage: function(canvasElement, inference, opacity=1.0) {
          // Get canvas context
          console.log("inference")
          console.log(inference)
          console.log("loading overlay")
          console.log("inference.value")
          console.log(inference.value)
          console.log(Object.keys(inference.value))

          var ctx = canvasElement.getContext("2d");
          var can_w = ctx.canvas.width
          var can_h = ctx.canvas.height
          var colors = ['red', 'blue', 'green', 'yellow', 'purple']
          var heatmap = new Image
          heatmap.id = "heatmap"
          console.log('_id')
          var i = new Image
          i.id = "image"
          i.onload = function() {
              console.log("creating thumbnail canvas image")
              var img_w = this.width
              var img_h = this.height
              var can_w = ctx.canvas.width //= 400
              var can_h = ctx.canvas.height //= 500
              // var hRatio = canvasElement.width / img_w    ;
              // var vRatio = canvasElement.height / img_h  ;
              console.log(`img_h ${img_h} img_w ${img_w} can_w ${can_w} can_h ${can_h}`)
              var vRatio = 1
              var hRatio = 1

              ctx.canvas.width = img_w
              ctx.canvas.height = img_h
              console.log(`img_h ${img_h} img_w ${img_w} can_w ${ctx.canvas.width} can_h ${ctx.canvas.height}`)
              var ratio = Math.min ( hRatio, vRatio )
              console.log('ratio')
              console.log(ratio)
              ctx.globalAlpha = 0.9;
              var centerShift_x = 0//( canvasElement.width - hRatio*img_w ) / 2;
              var centerShift_y = 0//( canvasElement.height - vRatio*img_h ) / 2;
              ctx.drawImage(i, 0, 0, img_w, img_h)//, centerShift_x,centerShift_y,img_w, img_h ) //, 100, 100 * imageObj.height / imageObj.width)
              if (inference.value['InferenceType'] == 'ObjectDetection') {
                // "classified":[{"confidence":0.9998242259025574,"ymax":153,"label":"helmet","xmax":236,"xmin":136,"ymin":8},{"confidence":0.7896438241004944,"ymax":492,"label":"safety_vest","xmax":314,"xmin":114,"ymin":143}]
                console.log("drawing boxes")
                console.log(inference.value['Class'])
                inference.value['Class'].split('|').map( (b, idx) => {
                  var coords = inference.value['Heatmap/Boxes'].split('|')[idx].split('-')
                  var o = {
                    xmin: coords[1],
                    xmax: coords[0],
                    ymin: coords[3],
                    ymax: coords[2],
                  }
                  var tl_x = o['xmin'] * hRatio
                  var tl_y = (o['ymin'] * vRatio)

                  var w = (o['xmax'] - o['xmin']) * hRatio
                  var h = (o['ymax'] - o['ymin']) * vRatio
                  ctx.lineWidth = "6";
                  ctx.strokeStyle = colors[idx % colors.length];
                  ctx.fillStyle = colors[idx % colors.length];
                  console.log(`xmin ${o['xmin']}, ymax ${o['ymax']}, hRatio ${hRatio} vRatio ${vRatio}`)
                  console.log(`w ${w}, h ${h}, tl_x ${tl_x}, tl_y ${tl_y} ` )
                  ctx.beginPath()
                  ctx.font = "40px Arial";
                  console.log(`writing class: ${b} ${o['xmin']} ${o['ymin']}`)
                  ctx.fillText(b, tl_x , tl_y )
                  ctx.rect( tl_x, tl_y, w, h )
                  ctx.stroke()
                })
              } else {
                heatmap.onload = function() {
                    console.log("drawing heatmap")
                    var img_w = this.width
                    var img_h = this.height
                    var hRatio = canvasElement.width / img_w    ;
                    var vRatio = canvasElement.height / img_h  ;
                    var ratio  = Math.max ( hRatio, vRatio )
                    ctx.globalAlpha = 0.4;
                    ctx.drawImage(heatmap, 0, 0, img_w, img_h, 0,0,img_w*ratio, img_h*ratio ) //, 100, 100 * imageObj.height / imageObj.width)
                    console.log("dims")
                    console.log(this.width)
                    console.log(this.height)
                    // TODO, add text based on class
                    // canvasElement.width = this.width
                    // canvasElement.height = this.height
                }
                heatmap.style.opacity = 0.1
                heatmap.style['z-index'] = 100
                console.log("inference['value']")
                console.log(inference['value'])
                if (inference['value']['ImageURL']) {
                  var s = inference['value']['ImageURL'].split('.')
                  var image_type = s[s.length - 1]
                }
                heatmap.src = 'data:image/' + image_type + ';base64,' + inference['value']['Heatmap/Boxes']
              }
          }
          if (Object.keys(inference['value']).includes('ImageURL')) {
            i.src = inference['value']['ImageURL']
          } else {
            console.log("writing thumbnail")
            console.log('data:image/' + 'png' + ';base64,' + inference['value']['Thumbnail'])
            i.src = 'data:image/' + 'png' + ';base64,' + inference['value']['Thumbnail']
          }

          console.log(`drawing image at ${inference['value']['ImageURL']}` )
          console.log(`canvasElement.width ${canvasElement.width}` )
          console.log(`canvasElement.height ${canvasElement.height}` )
      }
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
        inference_rows_original: [],
        inference_rows_filtered: [],
        query: '',
        tableData: [],
        // token: (localStorage['token'] || ''),
        // user_fields: [],
        // user_type: '',
        // user_input: [],
        input: [],
        func: '',
        title: '',
        src: '',
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
        csv_type: "",
        mobile_inference_headers: [
          "Thumbnail",
          "DataSetName",
          'Class',
          'Score',
          'Type',
          'FormattedDate',
          'Location'
        ],
        mapping: {
          "Class": "Metadata0",
          "Score": "Metadata1",
          "Heatmap/Boxes": "Metadata4",
          "ImageURL": "Thumbnail"
        },
        // inference_headers: [],
        inference_headers: [
          "ImageURL",
          "InferenceType",
          "Heatmap/Boxes",
          'Class',
          'Score',
          'Time'
        ],
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
      show() {
           this.$refs.view.method('show')();
      },
      dragOverHandler(ev) {
        console.log('File(s) in drop zone');
        ev.preventDefault();
      },
      dropHandler(ev) {
        console.log('File(s) dropped');
        // hideModal({'name': 'upload-modal'})
        // Prevent default behavior (Prevent file from being opened)
        ev.preventDefault();
        this.$data.filenames = []
        if (ev.dataTransfer.items) {
          // Use DataTransferItemList interface to access the file(s)
          for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
              var file = ev.dataTransfer.items[i].getAsFile();
              var s = file.text().then( (text) => {
                this.$data.inference_rows = []
                var rows = text.split(/\r\n|\n/)
                var h = rows[0].split(',');
                // if ( h.length > 10 ) {
                //   csv_type = "Mobile"
                // }
                // this.$data.inference_headers = h
                var min_row_length = 20 // TODO, added here in case of empty row / trailing spaces in csv.
                var row_data = {}
                var h_obj = h.map( (h) => { row_data[h] = "" } )
                if (h_obj) {
                  rows.slice(1).map( (r, r_idx) => {
                      var row_elements = r.split(',')
                      var row_data_copy = Object.create(row_data)
                      row_elements.map( (c, idx) => {
                        console.log(`adding column data ${c} ${idx}`)
                        row_data_copy[h[idx]] = c
                        // console.log( `${idx} / ${row.length - 1}` )

                        if ((idx == (row_elements.length - 1)) && (JSON.stringify(row_data_copy).length > min_row_length)) {
                          console.log(`appending row ${r_idx}`)
                          console.log(JSON.stringify(row_data_copy))
                          this.$data.inference_rows.push(row_data_copy)
                          this.$data.inference_rows_original.push(row_data_copy)
                        }
                      })
                  })
                }
              } )
              console.log('... file[' + i + '].name = ' + file.name);
              console.log("printing text")
              this.$data.filenames.push(file.name)
              this.$data.files.push(file)
             }
            }
          } else {
              // Use DataTransfer interface to access the file(s)
              for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
              }
            }
      },
      addFilter() {
        var filter_header = this.$data.filter_header
        var filter_compare_type = this.$data.filter_compare_type
        var filter_value = this.$data.filter_value
        // query column based on options
        // valid options are "less than", "greater than", "equal to", "contains"
        console.log("adding filter")
        console.log(filter_header, filter_compare_type, filter_value)
        var ts = Date.now()
        var filter = {}
        this.$data.activeFilters[ts] = [filter_header, filter_compare_type, filter_value] //.push( filter )
        if (filter_compare_type == 'less') {
          var filtered_rows = this.$data.inference_rows_original.filter(row => parseFloat(row[filter_header]) < parseFloat(filter_value))
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'greater') {
          var filtered_rows = this.$data.inference_rows_original.filter(row => parseFloat(row[filter_header]) > parseFloat(filter_value))
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'equal') {
          var filtered_rows = this.$data.inference_rows_original.filter(row => row[filter_header] == filter_value)
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
        } else if (filter_compare_type == 'contains') {
          var filtered_rows = this.$data.inference_rows_original.filter(row => row[filter_header].includes(filter_value))
          this.$data.inference_rows_filtered = filtered_rows
          console.log(`reduced to ${filtered_rows.length}`)
          // console.log("filtered to " this.$data.inference_rows_filtered)
        }
      },
      filterRows(){
        var filters = this.$data.activeFilters
        var filterFuncs = []
        var filtered_rows_total = this.$data.inference_rows_original
        Object.keys(filters).map( (ts, idx) => {
          // filters[ts]
          var filter_header = filters[ts][0]
          var filter_compare_type = filters[ts][1]
          var filter_value = filters[ts][2]

          var filter_less = (a, b) => a < b
          var filter_more = (a, b) => a > b
          var filter_equal = (a, b) => a == b
          var filter_contains = (a, b) => a.includes(b)

          // const filteredData = filters.reduce((d, f) => d.filter(f) , data)
          // if (filter_compare_type == 'less') {
          //   filterFuncs.append( filter_less() )
          // }

          if (filter_compare_type == 'less') {
            filtered_rows_total = filtered_rows_total.filter(row => parseFloat(row[filter_header]) < parseFloat(filter_value))
            if (idx == (filters.length - 1)) {
              this.$data.inference_rows = filtered_rows_total
            }
            // this.$data.inference_rows_filtered = filtered_rows
            // console.log(`reduced to ${filtered_rows.length}`)
          } else if (filter_compare_type == 'greater') {
            filtered_rows_total = filtered_rows_total.filter(row => parseFloat(row[filter_header]) > parseFloat(filter_value))
            if (idx == (filters.length - 1)) {
              this.$data.inference_rows = filtered_rows_total
            }
            // this.$data.inference_rows_filtered = filtered_rows
            // console.log(`reduced to ${filtered_rows.length}`)
          } else if (filter_compare_type == 'equal') {
            filtered_rows_total = filtered_rows_total.filter(row => row[filter_header] == filter_value)
            if (idx == (filters.length - 1)) {
              this.$data.inference_rows = filtered_rows_total
            }
            // this.$data.inference_rows_filtered = filtered_rows
            // console.log(`reduced to ${filtered_rows.length}`)
          } else if (filter_compare_type == 'contains') {
            filtered_rows_total = filtered_rows_total.filter(row => row[filter_header].includes(filter_value))
            if (idx == (filters.length - 1)) {
              this.$data.inference_rows = filtered_rows_total
            }
            // this.$data.inference_rows_filtered = filtered_rows
            // console.log(`reduced to ${filtered_rows.length}`)
            // console.log("filtered to " this.$data.inference_rows_filtered)
          }
        })
      },
      removeFilter(f){
        console.log(f)
        // this.$data.activeFilters[ts]
        // var matchingFilter = this.$data.activeFilters.filter(filter => { (filter[0] == f[0]) && (filter[1] == f[1]) && (filter[2] == f[2]) } )
        var aFilters = this.$data.activeFilters
        Object.keys(aFilters).map( (filter) => {
          if ((aFilters[filter][0] == f[0]) && (aFilters[filter][1] == f[1]) && (aFilters[filter][2] == f[2])) {
            console.log(`found matching filter, removing {filter}`)
            // this.$data.activeFilters.pop(aFilters)
            delete this.$data.activeFilters[filter]
            console.log(this.$data.activeFilters)
            var filtered_rows = this.$data.inference_rows_original.filter(row => row[filter_header].includes(filter_value))
            this.$data.inference_rows = filtered_rows
            // this.$data.inference_rows_filtered = filtered_rows
          }
        } )
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
        // this.$data.inference_rows_filtered = this.$data.inference_rows.filter(row => JSON.stringify(row.map( s =>  ([s.DataSetName, s.Class, s.Score, s.Type, s.FormattedDate, s.Location]) )  ).toLowerCase().includes(query.toLowerCase()))
        this.$data.inference_rows = this.$data.inference_rows_original.filter(row => JSON.stringify(([row.DataSetName, row.Class, row.Score, row.Type, row.FormattedDate, row.Location])  ).toLowerCase().includes(query.toLowerCase()))
        this.formatCircle()
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
          this.$data.inference_rows = this.$data.inference_rows.sort((a, b) => (a[column].toLowerCase() >= b[column].toLowerCase()) ? 1 : -1)
          this.$data.sortAscending = (! this.$data.sortAscending)
        } else {
          this.$data.inference_rows = this.$data.inference_rows.sort((a, b) => (a[column].toLowerCase() < b[column].toLowerCase()) ? 1 : -1)
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
      printElem() {
          // taken from https://stackoverflow.com/a/2255438
          var elem = "table_container"
          var mywindow = window.open('', 'PRINT', 'height=400,width=600');
          mywindow.document.write('<html><head><title>' + document.title  + '</title>');
          mywindow.document.write('</head><body >');
          mywindow.document.write('<h1>' + document.title  + '</h1>');
          mywindow.document.write(document.getElementById(elem).innerHTML);
          mywindow.document.write('</body></html>');
          mywindow.document.close(); // necessary for IE >= 10
          mywindow.focus(); // necessary for IE >= 10*/

          mywindow.print();
          mywindow.close();

          return true;
      },
      downloadReports2(){
        var pdf = new this.$jsPDF();
        var filename = "vis_insights_chart.pdf"

        if (this.$data.inference_rows_filtered.length > 0) {
          var rows = this.$data.inference_rows_filtered
          console.log("adding filtered rows to pdf")
        } else {
          var rows = this.$data.inference_rows
          console.log("adding all rows to pdf")
        }

        pdf.fromHTML( document.getElementById('table_container'), 10, 10, {'width': 180});
        // pdf.autoPrint();
        pdf.output("dataurlnewwindow"); // this opens a new popup,  after this the PDF opens the print window view but there are browser inconsistencies with how this is handled
        pdf.save(filename)

      },
      downloadReports1(){
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

        printDoc.autoPrint();
        printDoc.output("dataurlnewwindow"); // this opens a new popup,  after this the PDF opens the print window view but there are browser inconsistencies with how this is handled

        // doc.rect(40, 20, 10, 10); // filled square
        var headers = Object.keys(rows[0])

        // pdf.addPage('a4', 'p')
        var text_headers = this.$data.inference_headers //['DataSetName', 'Class', 'Score', 'URL', 'FormattedDate', 'Project' ]
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
              // if (Object.keys(row).includes('Thumbnail') && (row['Thumbnail'].length > 0)) {
              if (Object.keys(row).includes('Thumbnail') && (row['Thumbnail'].length > 0)) {
                var imageString = 'data:image/png;base64,' + row['Thumbnail'] // TODO, detect image typw
                // pdf.text(`image ${idx}`, 15, (40 * (idx + 1)))
                console.log(`image y ${(40 * (idx + 1 - currentPage))}`)
                pdf.addImage(imageString, 'PNG', 15, (50 * (( idx % inf_per_page ) + 1 )) , 45, 40)
              } else if (Object.keys(row).includes('ImageURL') && (row['ImageURL'].length > 0)) {

                var img = new Image();
                img.crossOrigin = 'Anonymous';
                img.onload = function() {

                  var canvas = document.createElement('canvas');
                  var ctx = canvas.getContext('2d');
                  canvas.height = this.naturalHeight;
                  canvas.width = this.naturalWidth;
                  ctx.drawImage(this, 0, 0);
                  var imageString = ctx.toDataURL()
                  pdf.addImage(imageString, 'PNG', 15, (50 * (( idx % inf_per_page ) + 1 )) , 45, 40)
                }
                console.log("creating canvas")
                console.log("setting url " + row['ImageURL'])
                img.src = row['ImageURL']
                if (img.complete || img.complete === undefined) {

                }
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
      formatCircle() {
        // console.log(this.$data.inferenceDetails)
        if (this.$data.inference_rows_filtered.length > 0) {
          var rows = this.$data.inference_rows_filtered
        } else {
          var rows = this.$data.inference_rows
        }

        console.log("generating line graph")
        // var detections = this.$data.inferenceDetails[inferenceId]
        // var objects = Object.keys(detections)
        var d = {
          values: [],
          labels: [],
          type: "pie",
          textinfo: "label+value",
          textposition: "outside",
          // automargin: true,
          showlegend: true
        }

        var count = {}
        rows.map( (r, idx) => {

          if (Object.keys(count).includes(r['Class'])) {
            count[r['Class']] += 1
          } else {
            count[r['Class']] = 1
          }

          if (idx == (rows.length - 1) ) {
            console.log("finished looping rows, format pie data")
            d['labels'] = Object.keys(count)
            Object.keys(count).map((l, l_idx) => {
              d['values'].push( count[l] )
              console.log("d")
              console.log(d)
              if (l_idx  == (Object.keys(count).length - 1 ) ) {
                this.$data.circleGraphData = [d]
                console.log("this.$data.circleGraphData")
                console.log(this.$data.circleGraphData)
              }
            })
            // d['values'] =
            // d['values']
            // d['labels'].push(r['Class'])

          }
        })

        // objects.map((o) => {
        //   d['values'].push(detections[o].reduce((a, b) => a + b, 0))
        //   d['labels'].push(o)
        //   console.log(d)
        // })

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
        console.log("config")
        console.log(Object.keys(config))
        this.$data.fields = config.fields
        this.$data.title = config.title
        if (Object.keys(config).includes('src')) {
          this.$data.src = config.src
          console.log("drawing image")
          this.$modal.show(config.name, {
            "fields": config.fields
          });
          return
        }
        else if (Object.keys(config).includes('inference')) {
          console.log("inference objdetected, drawing")
          this.$data.inference = config.inference
          this.$modal.show(config.name, {
            "fields": config.fields
          });
          return
        } else {
          this.$modal.show(config.name, {
            "fields": config.fields
          });
        }
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
    /* border: 2px dashed #eaecee; */
    /* width: 400px; */
    /* height: 300px; */
    margin: auto;
  }

  li {
    /* background: #cce5ff; */
    /* margin: 5px; */
    margin: 0;
    padding: 0;
    list-style-type: none;
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

<!-- <style lang="scss">
@import "./styles/carbon";
</style> -->

<!-- <style lang="scss" scoped>
  .md-card {
    width: 320px;
    margin: 40px;
    display: inline-block;
    vertical-align: top;
  }
</style> -->
