from handlers.instagram_handler import extract_profile_data, create_driver, login

if __name__ == "__main__":
    usernames = ["djacomospader"]

    driver = create_driver()
    try:
        login(driver)
        for username in usernames:
            data = extract_profile_data(driver, username)
            print(f"conteúdo: {data['header_section_4']}")
    finally:
        driver.quit()