
import { getSuccessToast, getErrorToast, TOAST_DURATION } from "../toast";

describe("Toast Configuration", () => {
  it("should create success toast with correct properties", () => {
    const toast = getSuccessToast("Success", "Test description");
    
    expect(toast).toMatchObject({
      variant: "default",
      title: "Success",
      description: "Test description",
      duration: TOAST_DURATION
    });
  });

  it("should create error toast with correct properties", () => {
    const toast = getErrorToast("Error", "Test description");
    
    expect(toast).toMatchObject({
      variant: "destructive",
      title: "Error",
      description: "Test description",
      duration: TOAST_DURATION
    });
  });

  it("should create toasts without description", () => {
    const successToast = getSuccessToast("Success");
    const errorToast = getErrorToast("Error");
    
    expect(successToast.description).toBeUndefined();
    expect(errorToast.description).toBeUndefined();
  });
});
