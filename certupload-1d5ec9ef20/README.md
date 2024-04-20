## IPFS Academic Certificate Storage App

This app allows you to securely store your academic certificates on IPFS using the Verbwire API.

### Features

* Upload academic certificates to IPFS
* Retrieve the uploaded certificate's IPFS URL
* Easy-to-use form interface

### Setup and Usage

**Requirements:**

* Node.js installed on your computer
* Vercel account (if you want to deploy the app)

**Steps:**

1. Clone the repository: `git clone https://github.com/your-username/ipfs-academic-certificate-storage-app.git`
2. Install the dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Open your browser and go to `http://localhost:3000` to view the app
5. To deploy the app to Vercel, follow the instructions in the `vercel.json` file

### How it Works

The app uses the Verbwire API to upload files to IPFS. The API provides a simple and reliable way to interact with IPFS.

When you select a file and click the "Upload Certificate" button, the app sends the file to the Verbwire API. The API then uploads the file to IPFS and returns the IPFS URL. The app then displays the IPFS URL to you.

### License

This app is licensed under the MIT License. See the `LICENSE` file for more details.