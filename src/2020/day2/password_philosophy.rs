use std::fs;
use std::path::{Path, PathBuf};

use regex::Regex;
use structopt::StructOpt;

type ValidatePasswordFn = fn(usize, usize, &char, &str) -> bool;

fn is_password_sled_valid(first: usize, second: usize, letter: &char, password: &str) -> bool {
    let letter_count = password.matches(letter).count();
    (first <= letter_count) && (letter_count <= second)
}

fn is_password_tobogan_valid(first: usize, second: usize, letter: &char, password: &str) -> bool {
    let password_chars = password.chars().collect();
    (password_chars[first - 1] == letter) ^ (password_chars[second - 1] == letter)
}

fn validate_passwords(passwords_path: &Path, is_password_valid_fn: ValidatePasswordFn) {
    let passwords_w_policy = fs::read_to_string(passwords_path)
        .expect(format!("No file found at: {:?}.", passwords_path).as_str())
        .lines();
    let mut valid_passwords: Vec<&str> = Vec::new();
    let separator = Regex::new(r"([ -:]+)").expect("Invalid regex");
    for password_w_policy in passwords_w_policy {
        let splits = separator.split(password_w_policy).collect();
        println!("{}", splits);
        valid_passwords.push(&password_w_policy)
    }
    println!("{} valid passwords were found:", valid_passwords.len());
}

/// AoC 2020 - Day 2: Password Philosophy
#[derive(StructOpt)]
struct Cli {
    /// The path to the passwords file to read
    #[structopt(parse(from_os_str))]
    passwords_path: PathBuf,
    /// The policy to use to determine if the password is valid
    password_policy: String,
}

fn main() {
    let args = Cli::from_args();
    if args.password_policy == "sled" {}
    let is_password_valid_fn = match args.password_policy.as_str() {
        "sled" => is_password_sled_valid,
        "tobogan" => is_password_tobogan_valid,
        _ => panic!(
            "The value for input argument `password_policy` is not supported. \
        It should be one of: ['sled', 'tobogan']."
        ),
    };
    validate_passwords(&args.passwords_path, is_password_valid_fn);
}
