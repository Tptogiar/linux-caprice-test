fn main() {
    let x4: u32 = 254;
    let x5: u32 = 255;
    let x6: u32 = 256;
    let x7: u32 = 257;

    let d4 = x4 / u8::MAX as u32;
    let d5 = x5 / u8::MAX as u32;
    let d6 = x6 / u8::MAX as u32;
    let d7 = x7 / u8::MAX as u32;

    println!("d4 = {}", d4);
    println!("d5 = {}", d5);
    println!("d6 = {}", d6);
    println!("d7 = {}", d7);

}
