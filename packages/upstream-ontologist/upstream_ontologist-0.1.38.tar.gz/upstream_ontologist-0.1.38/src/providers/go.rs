//! See https://golang.org/doc/modules/gomod-ref
use crate::{Certainty, GuesserSettings, ProviderError, UpstreamDatum, UpstreamDatumWithMetadata};
use log::debug;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

pub fn guess_from_go_mod(
    path: &Path,
    _settings: &GuesserSettings,
) -> std::result::Result<Vec<UpstreamDatumWithMetadata>, ProviderError> {
    let file = File::open(path).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut results = Vec::new();

    for line in reader.lines().map_while(Result::ok) {
        if line.starts_with("module ") {
            let modname = match line.trim().split_once(' ') {
                Some((_, modname)) => modname,
                None => {
                    debug!("Failed to parse module name from line: {}", line);
                    continue;
                }
            };
            results.push(UpstreamDatumWithMetadata {
                datum: UpstreamDatum::Name(modname.to_owned()),
                certainty: Some(Certainty::Certain),
                origin: Some(path.into()),
            });
        }
    }

    Ok(results)
}
