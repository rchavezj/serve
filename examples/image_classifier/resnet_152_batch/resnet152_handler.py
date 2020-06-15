import torch

from ts.torch_handler.image_classifier import ImageClassifier


class BatchImageClassifier(ImageClassifier):
    """
    BatchImageClassifier handler class. This handler takes list of images
    and returns a corresponding list of classes

    Here methods preprocess() and postprocess() have been overridden while others are reused from parent class.
    """

    def preprocess(self, request):
        """
        Preprocesses images in request using base class preprocess method and returns
        concatenated tensor of all images
        """
        image_tensor = None

        for idx, data in enumerate(request):
            input_image = super(BatchImageClassifier, self).preprocess([data])
            if input_image.shape is not None:
                if image_tensor is None:
                    image_tensor = input_image
                else:
                    image_tensor = torch.cat((image_tensor, input_image), 0)

        return image_tensor

    def postprocess(self, inference_output):
        num_rows, num_cols = inference_output.shape
        output_classes = []
        self.set_max_result_classes(1)
        for i in range(num_rows):
            out = inference_output[i].unsqueeze(0)
            output_classes.append(super(BatchImageClassifier, self).postprocess(out))
        return output_classes
