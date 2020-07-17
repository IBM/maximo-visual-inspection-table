# Generate and visualize video analytics using IBM Maximo Visual Inspection

In this Code Pattern we will demonstrate a dashboard that'll enable users to extract image analysis data from an IBM Maximo Visual Inspection instance. This extracted data can be filtered and viewed within an interactive table. The displayed data can also be exported as a PDF report.

When the reader has completed this Code Pattern, they will understand how to extract information from an IBM Maximo Visual Inspection instance as a CSV file, and how to visualize and filter the data within a web browser.

This code pattern is targeted towards users who have uploaded images to an IBM Maximo Visual Inspection instance via the Maximo Visual Inspection Mobile iOS application.


<!-- The intended audience for this Code Pattern -->


<img src="https://s3.us-east.cloud-object-storage.appdomain.cloud/staging-sombra/patterns/generate-dashboards-of-insights-from-inferred-results/images/flow.png">


#  Components

* [IBM Maximo Visual Inspection](https://www.ibm.com/us-en/marketplace/ibm-powerai-vision). This is an image analysis platform that allows you to build and manage computer vision models, upload and annotate images, and deploy apis to analyze images and videos.

Sign up for a trial account of IBM Maximo Visual Inspection [here](https://developer.ibm.com/linuxonpower/deep-learning-powerai/try-powerai/). This link includes options to provision a IBM Maximo Visual Inspection instance either locally on in the cloud.

* [IBM Maximo Visual Inspection Mobile](https://apps.apple.com/us/app/ibm-visual-inspector/id1486600972). This is an iOS application that allows users to upload images to Maximo Visual Inspection APIs from their mobile devices.


# Flow

1. Upload images using IBM Maximo Visual Inspection Mobile app
2. Train image inference model in IBM Maximo Visual Inspection via Maximo Visual Inspection Mobile app
3. Run Python script to extract inference data as CSV
4. Upload CSV to dashboard and view results

# Prerequisites

* An account on IBM Marketplace that has access to IBM Maximo Visual Inspection. This service can be provisioned [here](https://developer.ibm.com/linuxonpower/deep-learning-powerai/vision/access-registration-form/)


* Node.js

Skip to [Steps](#maximo-visual-table) if you already have node.js installed on your system.

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

1. [Upload images using IBM Maximo Visual Inspection Mobile app](#1-upload-images-using-ibm-visual-inspector-app)
2. [Clone repository](#2-clone-repository)
3. [Extract image data as CSV](#3-extract-image-data-as-csv)
4. [Load data into dashboard](#4-load-data-into-dashboard)

<!-- 5. [Create a Dashboard](#4-create-dashboard) -->
## 1. Upload images using IBM Maximo Visual Inspection Mobile app


[![Video Tutorial](https://i.imgur.com/OL5YQ1n.png)](https://www.youtube.com/watch?v=-jMIPusx6jg&feature=youtu.be&t=48)

Click image above to be guided through a step by step video tutorial.

- Download Maximo Visual Inspection Mobile from [App Store](https://apps.apple.com/us/app/ibm-visual-inspector/id1486600972)

- Open Maximo Visual Inspection Mobile app and register device

- Enter "Name" and "Location" and then click "Next"

- Enter the following IBM Maximo Visual Inspection credentials in the "Global Settings" section. These should be included in your Welcome Letter received when you activated the Visual Inspection service
  - URL
  - Username
  - Password

- Click "Save"

- Next, create a new project. Press the `+` icon in the upper right.

- Provide a inspection name

- Select "Create New Project".

- Select your targeted model and dataset.

- Click the "Capture" button to take and submit photos for analysis by the IBM Maximo Visual Inspection service.





## 2. Clone repository

Clone repository using the git cli

```
git clone https://github.com/IBM/maximo-visual-table
```

Navigate to the project folder

```
cd maximo-visual-table
```

## 3. Extract image inference data as CSV

Enter the `vision-inspector-dump` folder
```
cd vision-inspector-dump
```

Run the `visual_inspector_dump.py` python script which requires your Visual Inspection credentials (username, password, and url).


<!-- python3 visual_inspector_dump.py  --url https://<url>/<maximo-visual-ID> --user <username> --passwd <password>  --output test.csv -->
```
python visual_inspector_dump.py --user <username>
                                --passwd <password>
                                --url https://<url>/<maximo-visual-ID>
                                --output output.csv
```

See documentation for full list of options [here](#visual-inspector-dump)

If the cli is able to successfully authenticate to the Visual Inspection api, you'll see output similar to the following

<img src="https://i.imgur.com/ChbgPQw.png" />

## 4. Start dashboard


Return to top of project folder
```
cd ..
```

Enter `frontend` directory and install dependencies

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

<img src="https://i.imgur.com/mUQGn5R.png">

### Upload CSV file
Upload the .csv file previously generated in Step 3.

<img src="https://i.imgur.com/NfIeVS3.png" />


1. Click "Import CSV File"
2. Drag \*csv file to the "Upload Files" form
3. Click Upload CSV

After clicking "Upload" we should see a table like so.

<img src="https://i.imgur.com/xxZqlpf.png" />

This will show each inference as well as their associated metadata, such as time, score, detected class/object,  analysis type (object detection / classification), and more.

### Search
We can search through the table by entering a value in the search bar and pressing the Enter key on your keyboard. 6

So here, if we enter "dent" in the search bar, we'll see the list is trimmed down to 41 of 64 rows.

### Conditional filters

We can also filter the table results by adding one or more conditional statements. Some example conditional statements can be:
- Select where "score" is higher than 80.00
- Select where "date" include "2020"

So here we'll add a conditional statement by clicking the "Add/View Data Filters" button at the top of the page, and enter 3 parameters.

The options that are needed for the resulting form are
- The "Column" name (score, class, owner, etc)
- The conditional (greater than, equal to, contains)
- The value to compare each cell in the column to

We're entering "Score", "Greater", and "70.00", indicating that we only want to see data for inferences that have a score greater than 70.00.

<img src="https://i.imgur.com/7R26Aiy.png" />

Click "Add" and then we'll see the list trimmed down to 49 of 64 rows. Multiple filters can be active at the same time.


### Export PDF
We can also generate a PDF file containing a report of the table rows. This can be done by clicking the "Export PDF" button.

<img src="https://i.imgur.com/cqxvSmP.png" />





# Learn more

<!-- * **Watson IOT Platform Code Patterns**: Enjoyed this Code Pattern? Check out our other [Watson IOT Platform Code Patterns](https://developer.ibm.com/?s=Watson+IOT+Platform). -->

<!-- * **Knowledge Center**:Understand how this Python function can load data into  [Watson IOT Platform Analytics](https://www.ibm.com/support/knowledgecenter/en/SSQP8H/iot/analytics/as_overview.html) -->

# License

This code pattern is licensed under the Apache Software License, Version 2.  Separate third party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1 (DCO)](https://developercertificate.org/) and the [Apache Software License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache Software License (ASL) FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
