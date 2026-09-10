# React Compiler 점검과 호환성

React Compiler 적용 여부, 관련 Babel·ESLint 구성, 최적화 제외, 메모이제이션 회귀를 다룰 때 읽는다. 설정 유무, 실제 변환, 앱 동작을 별도로 검증한다.

## 환경과 Babel 구성

- `package.json` 선언과 실제 설치된 Expo, React, compiler plugin, Babel preset, React Hooks ESLint plugin, Reanimated/Worklets, NativeWind 버전을 확인한다. preset의 간접 의존성으로 제공되는 패키지도 구분한다.
- `experiments.reactCompiler`와 플랫폼별 compiler 옵션을 확인한다. SDK 54 이상에서는 Expo가 Babel 구성을 자동 처리하므로 수동 compiler 등록을 먼저 추가하지 않는다. 구형 SDK 또는 React에서는 해당 버전의 공식 안내로 runtime 패키지와 target을 확인한다.
- Babel은 preset을 역순으로 적용한다. 최상위 `plugins`만 보지 말고 preset이 펼쳐진 최종 목록에서 compiler가 한 번 포함되는지, Worklets 중복과 실행 순서를 확인한다. NativeWind와 Expo가 같은 플러그인을 자동 추가할 수 있다.
- Worklets는 compiler 뒤에서 실행되도록 구성하고 설치 버전의 순서 요구사항을 확인한다. 특정 프로젝트의 `worklets: false` 또는 `reanimated: false`를 복사하지 않는다. 자동 등록을 끄면 남은 등록 경로가 실제로 있는지 확인한다.

## 코드 작성과 제외 진단

- 컴파일러를 쓴다는 이유로 `memo`, `useMemo`, `useCallback`을 일괄 추가하거나 제거하지 않는다. 실제 컴파일 범위, 측정된 렌더 비용, 참조를 소비하는 코드의 계약을 확인한다. 앱의 정확성을 메모이제이션에 의존시키지 않는다.
- Effect에서만 필요한 객체는 가능하면 Effect 내부에서 만들고 실제 입력값을 의존성으로 선언한다. 의존성을 숨기거나 불필요한 의존성을 추가한 뒤 lint 억제로 맞추지 않는다.
- 지원되는 Reanimated 버전에서는 SharedValue의 `get()`/`set()`을 사용한다. 이 메서드도 렌더 중 읽기·쓰기를 허용하는 것은 아니다. 이벤트, Effect, 애니메이션 콜백 안에서 사용한다.

```ts
const handlePress = () => offset.set(withSpring(target));
const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ translateX: offset.get() }],
}));
```

- React Hooks recommended preset과 최종 규칙 수준을 확인한다. 컴파일러 진단이 통합된 `eslint-plugin-react-hooks`를 사용 중이면 구형 `eslint-plugin-react-compiler`의 중복 등록·의존성 제거를 검토한다.
- lint 통과를 위해 규칙을 전역으로 끄지 않는다. 네이티브 객체의 공식 변경 API나 지연 콜백처럼 분석 한계가 확인된 경우에만 근거와 함께 예외 범위를 좁힌다. ESLint 예외는 compiler 검사를 통과시켜 주지 않는다.
- 컴포넌트 내부의 React 규칙 억제 주석은 최적화 제외 원인이 될 수 있다. `"use no memo"`, 클래스 컴포넌트, 규칙 위반, 미지원 문법을 구분해 보고한다. 제외 진단을 모두 실행 오류로 취급하지 않는다.
- 회귀 원인을 분리해야 하면 영향받는 함수에만 `"use no memo"`를 임시 적용해 비교할 수 있다. 비교용 변경은 복원하고, 예외를 유지한다면 이유와 해제 조건을 남긴다. 미지원 문법을 없애기 위해 오류 처리나 정리 동작을 훼손하지 않는다.

## 실제 적용 검증

1. healthcheck는 호환성 사전 점검이다. 성공 수를 전체 앱의 최적화 보증으로 사용하지 않는다. 현재 프로젝트의 Babel 구성과 도구 내부 compiler 설정은 다를 수 있다.
2. 실제 Metro 출력은 읽을 수 있는 JS와 소스맵으로 확인한다. 프로젝트의 패키지 매니저에 맞춰 다음 명령을 사용한다. 출력 경로가 이미 있으면 다른 검증 전용 경로를 선택한다.

```sh
npx react-compiler-healthcheck@latest
npx expo export --platform ios --output-dir .compiler-check --no-bytecode --no-minify --source-maps
```

3. `compiler-runtime` 문자열만으로 적용을 판정하지 않는다. `_c(...)` 또는 `(0, _reactCompilerRuntime.c)(...)` 같은 변환된 캐시 호출을 찾고 소스맵으로 앱 파일에 연결한다. 의존성의 runtime 코드나 이미 컴파일된 라이브러리를 앱 최적화로 집계하지 않는다.
4. export가 막히면 대표 파일을 현재 preset과 Metro에 해당하는 caller 설정으로 변환한다. 단독 Babel CLI에는 Expo의 compiler 활성화 정보가 전달되지 않을 수 있으므로, 캐시 호출이 없다는 사실만으로 Metro 미적용을 단정하지 않는다.
5. Babel 구성을 바꿨다면 Metro를 캐시 초기화와 함께 재시작하고 앱을 완전히 재실행한다. 설정·플러그인 순서가 양쪽 플랫폼에 영향을 주면 iOS와 Android에서 화면 진입, 주요 동작, 렌더 갱신, 모션 및 관련 로그를 확인한다.
6. 직접 만든 검증용 출력만 삭제한다. 버전, 실행 명령, 앱 코드에 연결된 변환 근거, 제외 사유, 실제 실행 결과와 미검증 범위를 보고한다. 측정 수치와 제외 파일 목록은 실행 리포트에 남기고 스킬의 고정 기준으로 만들지 않는다.

## 공식 자료

- [Expo React Compiler](https://docs.expo.dev/guides/react-compiler/)
- [React Compiler 디버깅](https://react.dev/learn/react-compiler/debugging)
- [React useMemo](https://react.dev/reference/react/useMemo)
- [Reanimated SharedValue와 React Compiler](https://docs.swmansion.com/react-native-reanimated/docs/core/useSharedValue/#react-compiler-support)
