# Generate and visualize video analytics using IBM Visual Insights

In this Code Pattern we will demonstrate a dashboard that'll enable users to extract image analysis data from an IBM Visual Insights instance. This extracted data can be filtered and viewed within an interactive table. The displayed data can also be exported as a PDF report.

When the reader has completed this Code Pattern, they will understand how to extract information from an IBM Visual Insights instance as a CSV file, and how to visualize and filter the data within a web browser.

This code pattern is targeted towards users who have uploaded images to an IBM Visual Insights instance via the Visual Inspector iOS application.


<!-- The intended audience for this Code Pattern -->


<img src="https://i.imgur.com/TnAHWkQ.png">


#  Components

* [IBM Visual Insights](https://www.ibm.com/us-en/marketplace/ibm-powerai-vision). This is an image analysis platform that allows you to build and manage computer vision models, upload and annotate images, and deploy apis to analyze images and videos.

Sign up for a trial account of IBM Visual Insights [here](https://developer.ibm.com/linuxonpower/deep-learning-powerai/try-powerai/). This link includes options to provision a IBM Visual Insights instance either locally on in the cloud.

* [IBM Visual Inspector](https://apps.apple.com/us/app/ibm-visual-inspector/id1486600972). This is an iOS application that allows users to upload images to Visual Insights from their mobile devices.


# Flow

1. Upload images using IBM Visual Inspector app
2. Train image inference model in IBM Visual Insights via Visual Inspector app
3. Run Python script to extract inference data as CSV
4. Upload CSV to dashboard and view results

# Prerequisites

* An account on IBM Marketplace that has access to IBM Visual Insights. This service can be provisioned [here](https://developer.ibm.com/linuxonpower/deep-learning-powerai/vision/access-registration-form/)


* Node.js

Skip to [Steps](#visual-insights-table) if you already have node.js installed on your system.

### Install Node.js packages

If expecting to run this application locally, please install [Node.js](https://nodejs.org/en/) and NPM. Windows users can use the installer at the link [here](https://nodejs.org/en/download/).

If you're using Mac OS X or Linux, and your system requires additional versions of node for other projects, we'd suggest using [nvm](https://github.com/creationix/nvm) to easily switch between node versions. Install nvm with the following commands.

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```


```bash
# Place next three lines in ~/.bash_profile
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```


```bash
nvm install v8.9.0
nvm use 8.9.0
```


# Steps

Follow these steps to setup and run this Code Pattern.

1. [Upload images using IBM Visual Inspector app](#1-upload-images-using-ibm-visual-inspector-app)
2. [Clone repository](#2-clone-repository)
3. [Extract image data as CSV](#3-extract-image-data-as-csv)
4. [Load data into dashboard](#4-load-data-into-dashboard)

<!-- 5. [Create a Dashboard](#4-create-dashboard) -->
## 1. Upload images using IBM Visual Inspector app

[![](https://img.youtube.com/vi/jMIPusx6jg/0.jpg)](https://www.youtube.com/watch?v=-jMIPusx6jg&feature=youtu.be&t=48)


## 2. Clone repository

Clone repository using the git cli

```
git clone https://github.com/IBM/visual-insights-table
```

Navigate to the project folder

```
cd visual-insights-table
```

## 3. Extract image data as CSV

Enter the `vision-inspector-dump` folder
```
cd vision-inspector-dump
```

Run the `visual_inspector_dump.py` python script which requires your visual insights credentials (username, password, and url).


<!-- python3 visual_inspector_dump.py  --url https://<url>/<visual-insights-ID> --user <username> --passwd <password>  --output test.csv -->
```
python visual_inspector_dump.py --user <username>
                                --passwd <password>
                                --url https://<url>/<visual-insights-ID>
                                --output output.csv
```

See documentation for full list of options [here](#visual-inspector-dump)

If the cli is able to successfully authenticate to the visual insights api, you'll see output similar to the following

<img src="https://i.imgur.com/ChbgPQw.png" />

## 4. Start dashboard

Install frontend dependencies

```
cd frontend
npm install
```

After installing the prerequisites, we can start the dashboard application.

Run the following to start the frontend UI
```
cd frontend
npm run serve
```

Confirm you can access the Dashboard UI at [http://localhost:8080](http://localhost:8080).

<img src="https://i.imgur.com/5mKNIOL.png">

Upload the .csv file previously generated in Step 3.


<img src="https://i.imgur.com/NfIeVS3.png" />


1. Click "Import CSV File"
2. Drag \*csv file to the "Upload Files" form
3. Click Upload CSV

After clicking "Upload" we should be able to see a table like so.

<img src="https://i.imgur.com/xxZqlpf.png" />


# Learn more

<!-- * **Watson IOT Platform Code Patterns**: Enjoyed this Code Pattern? Check out our other [Watson IOT Platform Code Patterns](https://developer.ibm.com/?s=Watson+IOT+Platform). -->

<!-- * **Knowledge Center**:Understand how this Python function can load data into  [Watson IOT Platform Analytics](https://www.ibm.com/support/knowledgecenter/en/SSQP8H/iot/analytics/as_overview.html) -->

# License

This code pattern is licensed under the Apache Software License, Version 2.  Separate third party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1 (DCO)](https://developercertificate.org/) and the [Apache Software License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache Software License (ASL) FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
