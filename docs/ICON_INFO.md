# Integration Icon Information

## Current Icon Files

Your integration has icon files in two locations:

### Repository Root (for HACS):
```
/
├── icon.png       # 256x256 PNG - HACS will use this
├── icon@2x.png    # 512x512 PNG (high-DPI)
├── logo.png       # 256x256 PNG (alternative)
└── logo@2x.png    # 512x512 PNG (alternative high-DPI)
```

### Integration Folder (for Home Assistant):
```
custom_components/villages_events/
├── icon.png       # 256x256 PNG
├── icon@2x.png    # 512x512 PNG (high-DPI)
├── logo.png       # 256x256 PNG (alternative)
└── logo@2x.png    # 512x512 PNG (alternative high-DPI)
```

## Where Icons Are Used

### ✅ Working Now:
- **HACS**: If you publish to HACS, these icons will display in the HACS store
- **Documentation**: Icons can be referenced in README and docs
- **Entity Icons**: Individual entities use MDI icons (defined in code)

### ❌ Not Working (By Design):
- **Home Assistant Integrations Page**: Custom integrations don't show custom icons here by default
- This is a Home Assistant limitation, not an issue with your integration

## Why Custom Icons Don't Show in HA

Home Assistant's Integrations page only displays icons for:
1. **Core integrations** (built into Home Assistant)
2. **Integrations in the brands repository** (official brand logos)

Custom integrations installed locally or via HACS show a generic icon in the Integrations page.

## How to Get Your Icon in Home Assistant

### Option 1: Add to Home Assistant Brands Repository (Recommended)

This is the official way to add your integration's icon to Home Assistant:

1. **Fork the repository**:
   - Go to: https://github.com/home-assistant/brands
   - Click "Fork"

2. **Add your icons**:
   ```
   brands/
   └── custom_integrations/
       └── villages_events/
           ├── icon.png       # 256x256 PNG
           ├── icon@2x.png    # 512x512 PNG
           ├── logo.png       # 256x256 PNG
           └── logo@2x.png    # 512x512 PNG
   ```

3. **Submit a Pull Request**:
   - Commit your changes
   - Push to your fork
   - Create a PR to the main repository
   - Wait for review and approval

4. **Requirements**:
   - Icons must be square (256x256 or 512x512)
   - PNG format with transparency
   - Follow Home Assistant brand guidelines
   - Integration must be publicly available

### Option 2: Publish to HACS

If you publish your integration to HACS:
1. Your icons will show in the HACS store
2. Users will see your icon when browsing HACS
3. The integration page in HA will still show generic icon

### Option 3: Wait for HA Updates

Home Assistant may add better custom integration icon support in the future.

## Entity Icons (Already Working)

Your entities already have icons defined in the code:

**Sensor entities**: `mdi:calendar-music`
```python
# In sensor.py
self._attr_icon = "mdi:calendar-music"
```

**Binary sensor entities**: `mdi:star-circle`
```python
# In binary_sensor.py
self._attr_icon = "mdi:star-circle"
```

These icons show up in:
- Entity cards
- Dashboards
- Entity lists
- Automations

## Summary

✅ **Your icons are correctly placed** for HACS and future use
✅ **Entity icons are working** (MDI icons in code)
❌ **Integration page icon** requires adding to Home Assistant brands repository

## Next Steps

If you want your icon to show in the Home Assistant Integrations page:
1. Publish your integration publicly (GitHub)
2. Submit icons to Home Assistant brands repository
3. Wait for PR approval

Otherwise, your current setup is perfect for HACS and entity icons!

## References

- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [Brand Guidelines](https://github.com/home-assistant/brands/blob/master/CONTRIBUTING.md)
- [Material Design Icons](https://materialdesignicons.com/)
