#include <Adafruit_NeoPixel.h>
#include <Arduino.h>
#include <cstdio>

namespace {
constexpr uint8_t kProtocolVersion = 0;
constexpr uint8_t kPressurePin = OPENPAW_PRESSURE_PIN;
constexpr uint8_t kPixelPin = OPENPAW_WS2812_PIN;
constexpr uint16_t kPixelCount = OPENPAW_WS2812_COUNT;
constexpr uint16_t kPressThreshold = OPENPAW_PRESS_THRESHOLD;
constexpr uint16_t kReleaseThreshold = OPENPAW_RELEASE_THRESHOLD;
constexpr uint32_t kDebounceMs = OPENPAW_DEBOUNCE_MS;
constexpr uint32_t kSerialWaitMs = 1500;

static_assert(kReleaseThreshold < kPressThreshold,
              "release threshold must be lower than press threshold");

Adafruit_NeoPixel pixels(kPixelCount, kPixelPin, NEO_GRB + NEO_KHZ800);
bool candidatePressed = false;
bool stablePressed = false;
uint32_t candidateChangedAtMs = 0;
uint32_t sequenceNumber = 0;
char tileId[32] = {};

bool pressureState(uint16_t sample, bool currentState) {
  if (!currentState && sample >= kPressThreshold) {
    return true;
  }
  if (currentState && sample <= kReleaseThreshold) {
    return false;
  }
  return currentState;
}

void setPixels(uint8_t red, uint8_t green, uint8_t blue) {
  const uint32_t color = pixels.Color(red, green, blue);
  pixels.fill(color);
  pixels.show();
}

void emitBase(const char* type) {
  Serial.print(F("{\"v\":"));
  Serial.print(kProtocolVersion);
  Serial.print(F(",\"type\":\""));
  Serial.print(type);
  Serial.print(F("\",\"tile_id\":\""));
  Serial.print(tileId);
  Serial.print(F("\",\"seq\":"));
  Serial.print(++sequenceNumber);
  Serial.print(F(",\"uptime_ms\":"));
  Serial.print(millis());
}

void emitEvent(const char* type, uint16_t pressure) {
  emitBase(type);
  Serial.print(F(",\"pressure_raw\":"));
  Serial.print(pressure);
  Serial.println('}');
}

void emitHello() {
  emitBase("tile.hello");
  Serial.print(
      F(",\"firmware\":\"0.1.0-dev\",\"hardware_revision\":\"prototype\","
        "\"capabilities\":[\"pressure\",\"ws2812b\"],\"provisioned\":true,"
        "\"pressure_unit\":\"adc_raw\""));
  Serial.println('}');
}
}  // namespace

void setup() {
  std::snprintf(tileId, sizeof(tileId), "tile-%s", rp2040.getChipID());
  analogReadResolution(12);
  pixels.begin();
  pixels.setBrightness(32);
  setPixels(0, 0, 16);

  Serial.begin(115200);
  const uint32_t serialStartedAt = millis();
  while (!Serial && millis() - serialStartedAt < kSerialWaitMs) {
    delay(1);
  }

  const uint16_t sample = analogRead(kPressurePin);
  candidatePressed = pressureState(sample, false);
  stablePressed = candidatePressed;
  candidateChangedAtMs = millis();
  emitHello();
}

void loop() {
  const uint32_t now = millis();
  const uint16_t pressure = analogRead(kPressurePin);
  const bool sampledPressed = pressureState(pressure, candidatePressed);

  if (sampledPressed != candidatePressed) {
    candidatePressed = sampledPressed;
    candidateChangedAtMs = now;
  }

  if (candidatePressed != stablePressed &&
      now - candidateChangedAtMs >= kDebounceMs) {
    stablePressed = candidatePressed;
    setPixels(stablePressed ? 0 : 0, stablePressed ? 64 : 0,
              stablePressed ? 16 : 16);
    emitEvent(stablePressed ? "tile.pressed" : "tile.released", pressure);
  }

  delay(1);
}
