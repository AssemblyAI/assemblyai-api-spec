# Replace or establish new set of keyterms
client.update_configuration(keyterms_prompt=["Universal-3"])

# Remove keyterms and reset context biasing
client.update_configuration(keyterms_prompt=[])
