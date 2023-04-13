use lambda_runtime::{run, service_fn, Error, LambdaEvent};
use serde::{Deserialize, Serialize};
//use std::error::Error;
use std::fs::File;
use std::io::prelude::*;

#[derive(Deserialize)]
struct Request {
    stmt: String,
}

#[derive(Serialize)]
struct Response {
    req_id: String,
    content: String,
}

async fn list_contents() -> Result<String, Error> {
    let mut contents = String::new();
    for entry in std::fs::read_dir("/mnt/efs")? {
        let entry = entry?;
        let path = entry.path();
        if path.is_file() {
            let mut file = File::open(path)?;
            file.read_to_string(&mut contents)?;
        }
    }
    Ok(contents)
}

async fn function_handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    // Extract some useful info from the request
    let stmt = event.payload.stmt;
    //let files = list_files().await?;
    //let mut bag_of_words = HashMap::new();
    let content = list_contents().await?;
    //let bag_of_words = readfiles::tokenize(content.as_str());
    // Prepare the response
    let resp = Response {
        req_id: event.context.request_id,
        content: content,
    };

    // Return `Response` (it will be serialized to JSON automatically by the runtime)
    Ok(resp)
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        // disable printing the name of the module in every log line.
        .with_target(false)
        // disabling time is handy because CloudWatch will add the ingestion time.
        .without_time()
        .init();

    run(service_fn(function_handler)).await
}
