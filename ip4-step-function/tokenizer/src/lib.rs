use regex::Regex;
use std::collections::HashMap;

pub fn tokenize(text: &str) -> HashMap<String, usize> {
    let re = Regex::new(r"[^\p{L}]+").unwrap(); // matches any non-letter character
                                                //re.split(text).collect()
    let mut bag_of_words = HashMap::new();
    for token in re.split(text) {
        if !token.is_empty() {
            *bag_of_words.entry(token.to_lowercase()).or_insert(0) += 1;
        }
    }
    return bag_of_words;
}
