# ToRadiant.py

This script fetches and parses the MMR (Matchmaking Rating) for a specific player in Valorant, and calculates the RR (Ranked Rating) required for the player to reach the Radiant rank.

## Dependencies

- You Can change The location if you are on windows, but by default we are relying on apache2 on linux.
- Apache2: Make sure you have Apache2 installed on your system.
- Firewall Clearance: Ensure that the necessary firewall rules are in place to allow communication with the API.


## Usage
Replace <puuid> with the player's PUUID and <region> with the player's region.
You might need to run as sudo or run chown for your file.

You can run the script with the following command:

```bash
python toradiant.py <puuid> <region>
```

For Example 
```bash
python toradiant.py a11edb49-8856-5948-9f07-7c9d010fa15e ap
```

## API Credits

This project utilizes the [HenrikDev API](https://app.swaggerhub.com/apis-docs/Henrik-3/HenrikDev-API/3.0.0#/). Please refer to their documentation for more information.

Apache2 and Firewall Clearance
The script writes the RR required to a file in the /var/www/html directory for static hosting with Apache2. Make sure Apache2 is installed and the /var/www/html directory is writable by the user running the script.

If you're running a firewall, you may need to allow traffic to the Apache2 server. On Ubuntu, you can do this with the following command:
```bash
sudo ufw allow 'Apache Full'
```