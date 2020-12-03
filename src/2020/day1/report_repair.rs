use std::fs;
use std::path::{Path, PathBuf};
use std::str::FromStr;

use itertools::Itertools;
use structopt::StructOpt;

fn report_repair(expense_report: &Path, combinations_length: u8) {
    let expense_report_vals: Vec<usize> = fs::read_to_string(expense_report)
        .expect(format!("No file found at: {:?}.", expense_report).as_ref())
        .lines()
        .map(|x| {
            usize::from_str(x).expect("Report expense entry couldn't be converted to `usize`.")
        })
        .collect();
    for vals in expense_report_vals
        .into_iter()
        .combinations(combinations_length as usize)
    {
        let sum: usize = vals.iter().sum();
        if sum == 2020 {
            let product: usize = vals.iter().product();
            println!(
                "Values {:?} sum to 2020 and multiplied give {}",
                vals, product
            )
        }
    }
}

/// AoC 2020 - Day 1: Report Repair
#[derive(StructOpt)]
struct Cli {
    /// The path to the report file to read
    #[structopt(parse(from_os_str))]
    report_path: PathBuf,
    /// The length of combinations of expenses to consider
    combinations_length: u8,
}

fn main() {
    let args = Cli::from_args();
    report_repair(&args.report_path, args.combinations_length);
}
