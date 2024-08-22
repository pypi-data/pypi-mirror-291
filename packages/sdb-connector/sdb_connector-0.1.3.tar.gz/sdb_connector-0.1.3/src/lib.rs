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
fn sdb_connector(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(select_measurement_data_with_db_connect, m)?)?;
    Ok(())
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn select_measurement_data_with_db_connect(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str) -> PyResult<()> {
    // Create a Tokio runtime and block on the async function
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(select_measurement_data_with_db_connect_async_exe(ip, port,user, pw, namespace, db_name, table_name,run_id)).unwrap();
    Ok(())
}

async fn select_measurement_data_with_db_connect_async_exe(ip: &str, port: &str,
     user: &str, pw:&str, namespace: &str, db_name: &str,
     table_name: &str, run_id: &str) -> Result<(), Box<dyn Error>> {
    let db_url = format!("ws://{}:8000/rpc", ip);
    let db = Surreal::new::<Ws>(format!("{}:{}", ip, port)).await?;
    db.signin(Root {
        username: &format!("{}", user),
        password: &format!("{}", pw),
    })
    .await?;
    db.use_ns(&format!("{}", &namespace)).use_db(&format!("{}", &db_name)).await?;
    let result_query = format!("SELECT * FROM {} WHERE run_id = {} ORDER BY timestamp ASC", table_name, run_id);
    let result = db.query(&result_query).await?;
    println!("Result: {:?}", result);
    Ok(())
}


