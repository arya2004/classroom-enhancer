export async function POST(req) {
  try {
    const body = await req.formData();
    const file = body.get("uploadedFile");

    const form = new FormData();
    form.append("filePath", file);

    const options = {
      method: "POST",
      headers: {
        accept: "application/json",
        "X-API-Key": process.env.VERBWIRE_API_KEY,
      },
      body: form,
    };

    const response = await fetch(
      "https://api.verbwire.com/v1/nft/store/file",
      options
    );
    const data = await response.json();

    if (data?.ipfs_storage?.ipfs_url) {
      return new Response(
        JSON.stringify({ ipfsUrl: data.ipfs_storage.ipfs_url })
      );
    } else {
      throw new Error("IPFS URL not found in the response");
    }
  } catch (error) {
    console.error(error);
    return new Response(JSON.stringify({ error: "Error handling file" }), {
      status: 500,
    });
  }
}