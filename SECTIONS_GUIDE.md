# Interactive Poster Sections Guide

This feature allows you to highlight different sections  of the poster image at specific times during audio playback.

## How It Works

1. **JSON Configuration**: All section definitions are stored in `static/sections.json`
2. **Time-Synced**: Sections highlight automatically based on audio playback time
3. **Visual Editor**: Use the "Edit Sections" button to visually adjust sections
4. **Customizable**: Change position, size, color, and transparency for each section

## JSON Structure

Edit `static/sections.json` to configure your sections:

```json
{
  "sections": [
    {
      "id": "section1",
      "name": "Top Building",
      "startTime": 5,
      "endTime": 15,
      "position": {
        "x": 150,
        "y": 80
      },
      "size": {
        "width": 250,
        "height": 120
      },
      "color": "#7dd3fc",
      "transparency": 0.4,
      "borderColor": "#7dd3fc",
      "borderWidth": 3
    }
  ]
}
```

## Section Properties

- **id**: Unique identifier for the section
- **name**: Display name (shown on hover)
- **startTime**: When to start highlighting (in seconds)
- **endTime**: When to stop highlighting (in seconds)
- **position**: 
  - `x`: Left position in pixels
  - `y`: Top position in pixels
- **size**:
  - `width`: Width in pixels
  - `height`: Height in pixels
- **color**: Hex color code for the highlight (e.g., `#7dd3fc`)
- **transparency**: Opacity value from 0 to 1 (e.g., `0.4` = 40% transparent)
- **borderColor**: Hex color for the border
- **borderWidth**: Border thickness in pixels

## Using the Visual Editor

1. **Click "Edit Sections"** button below the poster
2. **All sections become visible** with resize handles
3. **Drag sections** to reposition them
4. **Drag corner handles** to resize
5. **Double-click a section** to edit color and transparency
6. **Click "Save Sections"** when done to save changes

## Tips

- **Position Accuracy**: Use pixel coordinates that match your poster dimensions
- **Timing**: Sync `startTime` and `endTime` with your audio narration
- **Colors**: Use contrasting colors for better visibility
  - Blue: `#7dd3fc`
  - Purple: `#a855f7`
  - Orange: `#f97316`
  - Green: `#10b981`
- **Transparency**: 0.3-0.5 works well for most cases
- **Border Width**: 2-4 pixels is recommended

## Example Use Case

If you're explaining a poster with multiple layers:
1. Section 1 highlights at 5-15s when you explain the top building
2. Section 2 highlights at 16-30s for the middle layer
3. Section 3 highlights at 31-45s for the data lake
4. Section 4 highlights at 46-60s for communication layer

## API Endpoints

The app exposes two endpoints for programmatic access:

- **GET** `/api/sections` - Retrieve current sections configuration
- **POST** `/api/sections` - Save sections configuration

## Troubleshooting

**Sections not appearing?**
- Check that `static/sections.json` exists and is valid JSON
- Verify position/size values match your poster dimensions
- Ensure audio is playing (sections only show during playback)

**Sections in wrong position?**
- Use the visual editor to adjust positions
- Remember coordinates are in pixels, not percentages
- Check that your poster image loaded correctly

**Can't save changes?**
- Ensure the Flask app has write permissions to `static/` folder
- Check browser console for error messages
