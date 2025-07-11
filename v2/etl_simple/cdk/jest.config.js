module.exports = {
  testEnvironment: "node",
  roots: ["<rootDir>"],
  testMatch: ["**/*.test.ts"],
  transform: {
    "^.+\\.tsx?$": "ts-jest"
  },
  moduleNameMapper: {
    "^@cdkConstructs/(.*)$": "<rootDir>/../../cdk-constructs/$1"
  },
  preset: "ts-jest"
}
