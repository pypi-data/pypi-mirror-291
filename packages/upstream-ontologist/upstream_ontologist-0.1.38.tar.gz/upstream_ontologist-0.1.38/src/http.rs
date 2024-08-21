// Too aggressive?
const DEFAULT_URLLIB_TIMEOUT: u64 = 3;

pub fn build_client() -> reqwest::blocking::ClientBuilder {
    reqwest::blocking::Client::builder()
        .user_agent(crate::USER_AGENT)
        .timeout(std::time::Duration::from_secs(DEFAULT_URLLIB_TIMEOUT))
}
