import evidently
print("Searching for DataDriftPreset...")
if hasattr(evidently, 'DataDriftPreset'):
    print("Found in root: from evidently import DataDriftPreset")
else:
    try:
        from evidently import presets
        print("Found in presets: from evidently.presets import DataDriftPreset")
    except ImportError:
        print("Could not find presets module.")