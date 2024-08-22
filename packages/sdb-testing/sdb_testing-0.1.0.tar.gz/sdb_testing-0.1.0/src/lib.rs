use surrealdb::Surreal;
use surrealdb::opt::auth::Root;
use surrealdb::sql::Value;
use surrealdb::engine::remote::ws::Client;
use surrealdb::engine::remote::ws::Ws;
use std::collections::HashMap;
use serde_json::Value as JsonValue;
use std::error::Error;
use std::time::Instant;
use pyo3::prelude::*;

#[pymodule]
fn sdb_testing(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(select_measuremnt_data, m)?)?;
    Ok(())
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn select_measuremnt_data(ip: &str, run_id: &str) -> PyResult<()> {
    // Create a Tokio runtime and block on the async function
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(select_udp_measurement_data(ip, run_id)).unwrap();
    Ok(())
}

async fn select_udp_measurement_data(ip: &str, run_id: &str) -> Result<(), Box<dyn Error>> {
    let db_url = format!("ws://{}:8000/rpc", ip);
    let db = Surreal::new::<Ws>("192.168.2.63:8000").await?;
    db.signin(Root {
        username: "root",
        password: "root",
    })
    .await?;
    db.use_ns("main").use_db("data").await?;
    let result_query = format!("SELECT * FROM amv_tag_49 WHERE run_id = {} ORDER BY timestamp ASC", run_id);
    let result = db.query(&result_query).await?;
    Ok(())
}


