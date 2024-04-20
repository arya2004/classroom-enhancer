'use client';
import React, { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [ipfsUrl, setIpfsUrl] = useState("");
  const [uploadError, setUploadError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIpfsUrl("");
    setUploadError("");
  };

  const uploadToIpfs = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file first!");
      return;
    }

    try {
      const form = new FormData();
      form.append("uploadedFile", file);
      let headersList = {
        Accept: "*/*",
        "User-Agent": "Thunder Client",
      };

      const response = await fetch("/api/verbwire", {
        method: "POST",
        body: form,
        headers: headersList,
      });

      if (response.ok) {
        const data = await response.json();
        setIpfsUrl(data.ipfsUrl);
        alert("File uploaded successfully!");
      } else {
        const data = await response.json();
        alert("Error uploading file or IPFS URL not found.");
        throw new Error(data.error || "Unknown error occurred");
      }
    } catch (err) {
      console.error(err);
      setUploadError("Error uploading file or IPFS URL not found.");
    }
  };

  return (
    <>
      <section className="min-h-screen bg-slate-900">
        <div className="mx-auto max-w-screen-xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8">
          <header className="text-center">
            <h1 className="text-3xl font-bold text-white sm:text-4xl">
              Upload Academic Certificate
            </h1>

            <p className="mx-auto mt-4 max-w-md text-gray-500">
              Upload your academic certificate to store it securely on IPFS.
            </p>
          </header>

          <div className="mt-6">
            <img
              src="https://images.unsplash.com/photo-1589330694653-ded6df03f754?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NDcwMzZ8MHwxfHNlYXJjaHwxfHxDZXJ0aWZpY2F0ZXN8ZW58MHwwfHx8MTcxMzU0NzUyOXww&ixlib=rb-4.0.3&q=80&w=1080"
              alt="Certificate"
              className="rounded-lg shadow-lg mx-auto max-h-[45vh]"
            />
          </div>

          <div className="mt-8">
            <form className="mx-auto max-w-lg" onSubmit={uploadToIpfs}>
              <div className="mb-4">
                <label
                  htmlFor="file-upload"
                  className="block text-sm font-medium text-gray-200"
                >
                  Select Certificate
                </label>
                <input
                  type="file"
                  id="file-upload"
                  className="mt-1 p-2 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                  onChange={handleFileChange}
                />
              </div>

              <div className="text-center">
                <button
                  type="submit"
                  className="mt-4 inline-block rounded bg-indigo-600 px-6 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 focus:outline-none focus:ring focus:ring-yellow-400"
                >
                  Upload Certificate
                </button>
              </div>
            </form>

            {ipfsUrl && !uploadError && (
              <div className="mt-4 text-center text-green-500">
                <p>Uploaded Successfully! IPFS URL:</p>
                <a
                  href={ipfsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className=" break-words"
                >
                  {ipfsUrl}
                </a>
              </div>
            )}

            {uploadError && (
              <div className="mt-4 text-center text-red-500">
                <p className="break-words">{uploadError}</p>
              </div>
            )}
          </div>
        </div>
      </section>
    </>
  );
}
